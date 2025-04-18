import importlib

PLUGIN_IDENTIFIER_PREFIX = "plugin:"


def discover_plugins_modules(plugins: list[str]):
    plugins_modules = []
    for dotted_path in plugins:
        try:
            module_path, class_name = dotted_path.rsplit(".", 1)
        except ValueError as err:
            raise ImportError(f"{dotted_path} doesn't look like a module path") from err

        module = importlib.import_module(module_path)
        plugins_modules.append(module.__package__)
    return plugins_modules
