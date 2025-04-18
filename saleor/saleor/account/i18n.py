import logging
from collections import defaultdict

import i18naddress
from django import forms
from django.core.exceptions import ValidationError
from django.forms import BoundField
from django.forms.models import ModelFormMetaclass
from django_countries import countries

from .i18n_valid_address_extension import VALID_ADDRESS_EXTENSION_MAP
from .models import Address
from .validators import validate_possible_number
from .widgets import DatalistTextWidget

COUNTRY_FORMS = {}
UNKNOWN_COUNTRIES = set()
ADDRESS_FIELDS_TO_LOG = ["country_area", "city_area", "city"]

AREA_TYPE = {
    "area": "Area",
    "county": "County",
    "department": "Department",
    "district": "District",
    "do_si": "Do/si",
    "eircode": "Eircode",
    "emirate": "Emirate",
    "island": "Island",
    "neighborhood": "Neighborhood",
    "oblast": "Oblast",
    "parish": "Parish",
    "pin": "PIN",
    "postal": "Postal code",
    "prefecture": "Prefecture",
    "province": "Province",
    "state": "State",
    "suburb": "Suburb",
    "townland": "Townland",
    "village_township": "Village/township",
    "zip": "ZIP code",
}

logger = logging.getLogger(__name__)


class PossiblePhoneNumberFormField(forms.CharField):
    """A phone input field."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.input_type = "tel"


class CountryAreaChoiceField(forms.ChoiceField):
    widget = DatalistTextWidget

    def valid_value(self, value):
        return True


class AddressMetaForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["country"]
        labels = {"country": "Country"}

    def clean(self):
        data = super().clean()
        return data


class AddressForm(forms.ModelForm):
    AUTOCOMPLETE_MAPPING = [
        ("first_name", "given-name"),
        ("last_name", "family-name"),
        ("company_name", "organization"),
        ("street_address_1", "address-line1"),
        ("street_address_2", "address-line2"),
        ("city", "address-level2"),
        ("postal_code", "postal-code"),
        ("country_area", "address-level1"),
        ("country", "country"),
        ("city_area", "address-level3"),
        ("phone", "tel"),
        ("email", "email"),
    ]

    class Meta:
        model = Address
        exclude = []
        labels = {
            "first_name": "Given name",
            "last_name": "Family name",
            "company_name": "Company or organization",
            "street_address_1": "Address",
            "street_address_2": "",
            "city": "City",
            "city_area": "District",
            "postal_code": "Postal code",
            "country": "Country",
            "country_area": "State or province",
            "phone": "Phone number",
        }
        placeholders = {
            "street_address_1": "Street address, P.O. box, company name",
            "street_address_2": "Apartment, suite, unit, building, floor, etc",
        }

    phone = PossiblePhoneNumberFormField(required=False)

    def __init__(self, *args, **kwargs):
        autocomplete_type = kwargs.pop("autocomplete_type", None)
        self.enable_normalization = kwargs.pop("enable_normalization", True)
        super().__init__(*args, **kwargs)
        # countries order was taken as defined in the model,
        # not being sorted accordingly to the selected language
        self.fields["country"].choices = sorted(  # type: ignore[attr-defined] # raw access to fields # noqa: E501
            COUNTRY_CHOICES, key=lambda choice: str(choice[1])
        )
        autocomplete_dict = defaultdict(lambda: "off", self.AUTOCOMPLETE_MAPPING)
        for field_name, field in self.fields.items():
            if autocomplete_type:
                autocomplete = f"{autocomplete_type} {autocomplete_dict[field_name]}"
            else:
                autocomplete = autocomplete_dict[field_name]
            field.widget.attrs["autocomplete"] = autocomplete
            field.widget.attrs["placeholder"] = (
                field.label if not hasattr(field, "placeholder") else field.placeholder
            )

    def clean(self):
        data = super().clean()
        if not data:
            return None
        phone = data.get("phone")
        country = data.get("country")
        if phone:
            try:
                data["phone"] = validate_possible_number(phone, country)
            except forms.ValidationError as error:
                self.add_error("phone", error)
        return data


class CountryAwareAddressForm(AddressForm):
    I18N_MAPPING: list[tuple[str, list[str]]] = [
        ("name", ["first_name", "last_name"]),
        ("street_address", ["street_address_1", "street_address_2"]),
        ("city_area", ["city_area"]),
        ("country_area", ["country_area"]),
        ("company_name", ["company_name"]),
        ("postal_code", ["postal_code"]),
        ("city", ["city"]),
        ("sorting_code", []),
        ("country_code", ["country"]),
    ]

    NOT_REQUIRED_FIELDS = ("street_address_2",)

    class Meta:
        model = Address
        exclude = []

    def add_field_errors(self, errors):
        field_mapping = dict(self.I18N_MAPPING)
        for field_name, error_code in errors.items():
            local_fields = field_mapping[field_name]
            for field in local_fields:
                if field in self.NOT_REQUIRED_FIELDS:
                    continue

                try:
                    error_msg = self.fields[field].error_messages[error_code]
                except KeyError:
                    error_msg = "This value is not valid for the address."
                self.add_error(field, ValidationError(error_msg, code=error_code))

    def validate_address(self, data):
        try:
            data["country_code"] = data.get("country", "")

            street_address_1 = data.get("street_address_1", "")
            street_address_2 = data.get("street_address_2", "")
            if street_address_1 or street_address_2:
                data["street_address"] = f"{street_address_1}\n{street_address_2}"

            self.substitute_invalid_values(data)
            normalized_data = i18naddress.normalize_address(data)
            if getattr(self, "enable_normalization", True):
                data = normalized_data
                del data["sorting_code"]
        except i18naddress.InvalidAddressError as exc:
            self.add_field_errors(exc.errors)
            self.log_errors()
        return data

    def clean(self):
        data = super().clean()
        return self.validate_address(data)

    @staticmethod
    def substitute_invalid_values(data):
        """Map invalid address names to the values accepted by i18naddress package."""
        country_code = data["country_code"]
        if not country_code:
            return
        if custom_names := VALID_ADDRESS_EXTENSION_MAP.get(country_code):
            for field_name, mapping in custom_names.items():
                actual_value = data.get(field_name, "").strip().lower()
                if actual_value in mapping:
                    data[field_name] = mapping[actual_value]

    def log_errors(self):
        if not self.data.get("skip_validation"):
            return

        errors = self.errors
        fields = {}
        for field, _ in errors.items():
            fields[field] = (
                self.data.get(field) if field in ADDRESS_FIELDS_TO_LOG else "invalid"
            )
        fields["country"] = self.data.get("country")
        logger.warning("Invalid address input: %s", fields)


def get_address_form_class(country_code):
    return COUNTRY_FORMS.get(country_code, AddressForm)


def get_form_i18n_lines(form_instance) -> list[list[BoundField]]:
    country_code = form_instance.i18n_country_code
    try:
        fields_order = i18naddress.get_field_order({"country_code": country_code})
    except ValueError:
        fields_order = i18naddress.get_field_order({})
    field_mapping = dict(form_instance.I18N_MAPPING)

    def _convert_to_bound_fields(form, i18n_field_names):
        bound_fields = []
        for field_name in i18n_field_names:
            local_fields = field_mapping[field_name]
            for local_name in local_fields:
                local_field = form_instance.fields[local_name]
                bound_field = BoundField(form, local_field, local_name)
                bound_fields.append(bound_field)
        return bound_fields

    if fields_order:
        return [_convert_to_bound_fields(form_instance, line) for line in fields_order]
    return []


def update_base_fields(form_class, i18n_rules):
    for field_name, label_value in AddressForm.Meta.labels.items():
        field = form_class.base_fields[field_name]
        field.label = label_value

    for field_name, placeholder_value in AddressForm.Meta.placeholders.items():
        field = form_class.base_fields[field_name]
        field.placeholder = placeholder_value

    if i18n_rules.country_area_choices:
        required = "country_area" in i18n_rules.required_fields
        form_class.base_fields["country_area"] = CountryAreaChoiceField(
            choices=i18n_rules.country_area_choices, required=required
        )

    labels_map = {
        "country_area": i18n_rules.country_area_type,
        "postal_code": i18n_rules.postal_code_type,
        "city_area": i18n_rules.city_area_type,
    }

    for field_name, area_type in labels_map.items():
        field = form_class.base_fields[field_name]
        field.label = AREA_TYPE[area_type]

    hidden_fields = i18naddress.KNOWN_FIELDS - i18n_rules.allowed_fields
    for field_name in hidden_fields:
        if field_name in form_class.base_fields:
            form_class.base_fields[field_name].widget = forms.HiddenInput()

    country_field = form_class.base_fields["country"]
    country_field.choices = COUNTRY_CHOICES


def construct_address_form(country_code, i18n_rules):
    class_name = f"AddressForm{country_code}"
    base_class = CountryAwareAddressForm
    form_kwargs = {
        "Meta": type("Meta", (base_class.Meta, object), {}),
        "formfield_callback": None,
        "i18n_country_code": country_code,
        "i18n_fields_order": property(get_form_i18n_lines),
    }
    class_ = ModelFormMetaclass(str(class_name), (base_class,), form_kwargs)
    update_base_fields(class_, i18n_rules)
    return class_


for country in countries.countries.keys():
    try:
        country_rules = i18naddress.get_validation_rules({"country_code": country})
    except ValueError:
        country_rules = i18naddress.get_validation_rules({})
        UNKNOWN_COUNTRIES.add(country)

COUNTRY_CHOICES = [
    (code, label)
    for code, label in countries.countries.items()
    if code not in UNKNOWN_COUNTRIES
]
# Sort choices list by country name
COUNTRY_CHOICES = sorted(COUNTRY_CHOICES, key=lambda choice: str(choice[1]))

for country, _label in COUNTRY_CHOICES:
    country_rules = i18naddress.get_validation_rules({"country_code": country})
    COUNTRY_FORMS[country] = construct_address_form(country, country_rules)
