from collections import defaultdict
from functools import partial, wraps

from promise import Promise

from ...core.middleware import Requestor
from ...plugins.manager import PluginsManager, get_plugins_manager
from ...plugins.models import EmailTemplate
from ..app.dataloaders import get_app_promise
from ..core import SaleorContext
from ..core.dataloaders import DataLoader


class EmailTemplatesByPluginConfigurationLoader(DataLoader[int, list[EmailTemplate]]):
    """Loads email templates by plugin configuration ID."""

    context_key = "email_template_by_plugin_configuration"

    def batch_load(self, keys):
        email_templates = EmailTemplate.objects.using(
            self.database_connection_name
        ).filter(plugin_configuration_id__in=keys)

        config_to_template = defaultdict(list)
        for et in email_templates:
            config_to_template[et.plugin_configuration_id].append(et)

        return [config_to_template[key] for key in keys]


class PluginManagerByRequestorDataloader(DataLoader[Requestor, PluginsManager]):
    context_key = "plugin_manager_by_requestor"

    def batch_load(self, keys):
        allow_replica = getattr(self.context, "allow_replica", True)
        return [get_plugins_manager(allow_replica, lambda: user) for user in keys]


class AnonymousPluginManagerLoader(DataLoader[None, PluginsManager]):
    context_key = "anonymous_plugin_manager"

    def batch_load(self, keys):
        # When modify this code, modify also code
        # in `saleor.core.auth_backend.PluginBackend.authenticate`

        allow_replica = getattr(self.context, "allow_replica", True)
        return [get_plugins_manager(allow_replica, None) for key in keys]


def plugin_manager_promise(context: SaleorContext, app) -> Promise[PluginsManager]:
    user = context.user
    requestor = app or user
    if requestor is None:
        return AnonymousPluginManagerLoader(context).load("Anonymous")
    return PluginManagerByRequestorDataloader(context).load(requestor)


def get_plugin_manager_promise(context: SaleorContext) -> Promise[PluginsManager]:
    app = get_app_promise(context).get()
    return plugin_manager_promise(context, app)


def plugin_manager_promise_callback(func):
    @wraps(func)
    def _wrapper(root, info, *args, **kwargs):
        return get_plugin_manager_promise(info.context).then(
            partial(func, root, info, *args, **kwargs)
        )

    return _wrapper
