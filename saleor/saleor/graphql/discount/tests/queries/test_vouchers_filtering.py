import datetime

import pytest
from django.utils import timezone
from freezegun import freeze_time

from .....discount import DiscountValueType
from .....discount.models import Voucher, VoucherCode
from ....tests.utils import get_graphql_content

QUERY_VOUCHERS_WITH_FILTER = """
    query ($filter: VoucherFilterInput!, ) {
      vouchers(first:5, filter: $filter){
        edges{
          node{
            id
            name
            startDate
          }
        }
      }
    }
"""


@pytest.mark.parametrize(
    ("voucher_filter", "start_date", "end_date", "count"),
    [
        (
            {"status": "ACTIVE"},
            timezone.now().replace(year=2015, month=1, day=1),
            timezone.now() + datetime.timedelta(days=365),
            2,
        ),
        (
            {"status": "EXPIRED"},
            timezone.now().replace(year=2015, month=1, day=1),
            timezone.now().replace(year=2018, month=1, day=1),
            1,
        ),
        (
            {"status": "SCHEDULED"},
            timezone.now() + datetime.timedelta(days=3),
            timezone.now() + datetime.timedelta(days=10),
            1,
        ),
    ],
)
def test_query_vouchers_with_filter_status(
    voucher_filter,
    start_date,
    end_date,
    count,
    staff_api_client,
    permission_manage_discounts,
):
    vouchers = Voucher.objects.bulk_create(
        [
            Voucher(
                name="Voucher1",
                start_date=timezone.now(),
            ),
            Voucher(
                name="Voucher2",
                start_date=start_date,
                end_date=end_date,
            ),
        ]
    )
    VoucherCode.objects.bulk_create(
        [
            VoucherCode(code="abc", voucher=vouchers[0]),
            VoucherCode(code="123", voucher=vouchers[1]),
        ]
    )
    variables = {"filter": voucher_filter}
    response = staff_api_client.post_graphql(
        QUERY_VOUCHERS_WITH_FILTER, variables, permissions=[permission_manage_discounts]
    )
    content = get_graphql_content(response)
    data = content["data"]["vouchers"]["edges"]
    assert len(data) == count


@pytest.mark.parametrize(
    ("voucher_filter", "count"),
    [
        ({"timesUsed": {"gte": 1, "lte": 5}}, 1),
        ({"timesUsed": {"lte": 3}}, 2),
        ({"timesUsed": {"gte": 2}}, 1),
    ],
)
def test_query_vouchers_with_filter_times_used(
    voucher_filter,
    count,
    staff_api_client,
    permission_manage_discounts,
):
    vouchers = Voucher.objects.bulk_create(
        [
            Voucher(name="Voucher1"),
            Voucher(name="Voucher2"),
        ]
    )
    VoucherCode.objects.bulk_create(
        [
            VoucherCode(code="abc", voucher=vouchers[0]),
            VoucherCode(code="123", used=2, voucher=vouchers[1]),
        ]
    )
    variables = {"filter": voucher_filter}
    response = staff_api_client.post_graphql(
        QUERY_VOUCHERS_WITH_FILTER, variables, permissions=[permission_manage_discounts]
    )
    content = get_graphql_content(response)
    data = content["data"]["vouchers"]["edges"]
    assert len(data) == count


@pytest.mark.parametrize(
    ("voucher_filter", "count"),
    [
        ({"started": {"gte": "2019-04-18T00:00:00+00:00"}}, 1),
        ({"started": {"lte": "2012-01-14T00:00:00+00:00"}}, 1),
        (
            {
                "started": {
                    "lte": "2012-01-15T00:00:00+00:00",
                    "gte": "2012-01-01T00:00:00+00:00",
                }
            },
            1,
        ),
        ({"started": {"gte": "2012-01-03T00:00:00+00:00"}}, 2),
    ],
)
def test_query_vouchers_with_filter_started(
    voucher_filter,
    count,
    staff_api_client,
    permission_manage_discounts,
):
    vouchers = Voucher.objects.bulk_create(
        [
            Voucher(name="Voucher1"),
            Voucher(
                name="Voucher2",
                start_date=timezone.now().replace(year=2012, month=1, day=5),
            ),
        ]
    )
    VoucherCode.objects.bulk_create(
        [
            VoucherCode(code="abc", voucher=vouchers[0]),
            VoucherCode(code="123", voucher=vouchers[1]),
        ]
    )

    variables = {"filter": voucher_filter}
    response = staff_api_client.post_graphql(
        QUERY_VOUCHERS_WITH_FILTER, variables, permissions=[permission_manage_discounts]
    )
    content = get_graphql_content(response)
    data = content["data"]["vouchers"]["edges"]
    assert len(data) == count


@pytest.mark.parametrize(
    ("voucher_filter", "count", "discount_value_type"),
    [
        ({"discountType": "PERCENTAGE"}, 1, DiscountValueType.PERCENTAGE),
        ({"discountType": "FIXED"}, 2, DiscountValueType.FIXED),
    ],
)
def test_query_vouchers_with_filter_discount_type(
    voucher_filter,
    count,
    discount_value_type,
    staff_api_client,
    permission_manage_discounts,
):
    vouchers = Voucher.objects.bulk_create(
        [
            Voucher(
                name="Voucher1",
                discount_value_type=DiscountValueType.FIXED,
            ),
            Voucher(
                name="Voucher2",
                discount_value_type=discount_value_type,
            ),
        ]
    )
    VoucherCode.objects.bulk_create(
        [
            VoucherCode(code="abc", voucher=vouchers[0]),
            VoucherCode(code="123", voucher=vouchers[1]),
        ]
    )
    variables = {"filter": voucher_filter}
    response = staff_api_client.post_graphql(
        QUERY_VOUCHERS_WITH_FILTER, variables, permissions=[permission_manage_discounts]
    )
    content = get_graphql_content(response)
    data = content["data"]["vouchers"]["edges"]
    assert len(data) == count


@pytest.mark.parametrize(
    ("voucher_filter", "count"), [({"search": "Big"}, 1), ({"search": "GIFT"}, 2)]
)
def test_query_vouchers_with_filter_search(
    voucher_filter,
    count,
    staff_api_client,
    permission_manage_discounts,
):
    vouchers = Voucher.objects.bulk_create(
        [
            Voucher(name="The Biggest Voucher"),
            Voucher(name="Voucher2"),
        ]
    )
    VoucherCode.objects.bulk_create(
        [
            VoucherCode(code="GIFT", voucher=vouchers[0]),
            VoucherCode(code="GIFT-COUPON", voucher=vouchers[1]),
        ]
    )
    variables = {"filter": voucher_filter}
    response = staff_api_client.post_graphql(
        QUERY_VOUCHERS_WITH_FILTER, variables, permissions=[permission_manage_discounts]
    )
    content = get_graphql_content(response)
    data = content["data"]["vouchers"]["edges"]
    assert len(data) == count


@freeze_time("2020-03-18 12:00:00")
@pytest.mark.parametrize(
    ("start_date", "end_date", "used", "count"),
    [
        (
            timezone.now().replace(year=2018, month=1, day=1),
            timezone.now().replace(year=2019, month=1, day=1),
            0,
            2,
        ),
        (
            timezone.now().replace(year=2023, month=1, day=1),
            timezone.now().replace(year=2024, month=1, day=1),
            0,
            0,
        ),
        (
            timezone.now().replace(year=2023, month=1, day=1),
            None,
            0,
            0,
        ),
        (
            timezone.now().replace(year=2019, month=1, day=1),
            timezone.now().replace(year=2021, month=1, day=1),
            0,
            0,
        ),
        (
            timezone.now().replace(year=2019, month=1, day=1),
            timezone.now().replace(year=2021, month=1, day=1),
            2,
            1,
        ),
        (
            timezone.now().replace(year=2019, month=1, day=1),
            timezone.now().replace(year=2021, month=1, day=1),
            110,
            2,
        ),
    ],
)
def test_query_vouchers_with_filter_status_expired(
    start_date,
    end_date,
    used,
    count,
    staff_api_client,
    permission_manage_discounts,
):
    # given
    vouchers = Voucher.objects.bulk_create(
        [
            Voucher(
                name="Voucher1",
                start_date=timezone.now(),
            ),
            Voucher(
                name="Voucher2",
                start_date=start_date,
                end_date=end_date,
                usage_limit=5,
            ),
            Voucher(
                name="Voucher3",
                start_date=start_date,
                end_date=end_date,
                usage_limit=100,
            ),
        ]
    )
    VoucherCode.objects.bulk_create(
        [
            VoucherCode(code="code-A", voucher=vouchers[0]),
            VoucherCode(code="code-B", voucher=vouchers[0]),
            VoucherCode(code="code-1", voucher=vouchers[1], used=3),
            VoucherCode(code="code-2", voucher=vouchers[1], used=used),
            VoucherCode(code="code-abc", voucher=vouchers[2], used=used),
        ]
    )
    variables = {"filter": {"status": "EXPIRED"}}

    # whne
    response = staff_api_client.post_graphql(
        QUERY_VOUCHERS_WITH_FILTER, variables, permissions=[permission_manage_discounts]
    )
    content = get_graphql_content(response)

    # then
    data = content["data"]["vouchers"]["edges"]
    assert len(data) == count
