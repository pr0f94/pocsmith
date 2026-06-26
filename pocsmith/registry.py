from __future__ import annotations

from importlib import import_module

from pocsmith.modules.base import Module


MODULE_FILES = {
    "requests_session": "pocsmith.modules.requests_session",
    "multi_session": "pocsmith.modules.multi_session",
    "flask_server": "pocsmith.modules.flask_server",
    "queue_state": "pocsmith.modules.queue_state",
    "callback_value_handler": "pocsmith.modules.callback_value_handler",
    "proof_callback": "pocsmith.modules.proof_callback",
    "local_callback": "pocsmith.modules.local_callback",
    "cookie_callback": "pocsmith.modules.cookie_callback",
    "netcat_listener": "pocsmith.modules.netcat_listener",
    "json_registration": "pocsmith.modules.json_registration",
    "form_auth": "pocsmith.modules.form_auth",
    "json_auth": "pocsmith.modules.json_auth",
    "headers": "pocsmith.modules.headers",
    "token_extractor": "pocsmith.modules.token_extractor",
    "html_parser": "pocsmith.modules.html_parser",
    "csrf": "pocsmith.modules.csrf",
    "regex_extract": "pocsmith.modules.regex_extract",
    "base64_helpers": "pocsmith.modules.base64_helpers",
    "zip_builder": "pocsmith.modules.zip_builder",
    "file_upload": "pocsmith.modules.file_upload",
    "websocket_client": "pocsmith.modules.websocket_client",
    "websocket_async": "pocsmith.modules.websocket_async",
    "bruteforce_loop": "pocsmith.modules.bruteforce_loop",
}

MODULE_ORDER = tuple(MODULE_FILES)


def load_modules() -> dict[str, Module]:
    modules = {}
    for name, module_path in MODULE_FILES.items():
        loaded = import_module(module_path)
        modules[name] = loaded.MODULE
    return modules


def alias_map(modules: dict[str, Module]) -> dict[str, str]:
    aliases = {}
    for name, module in modules.items():
        for alias in module.aliases:
            aliases[alias] = name
    return aliases


def aliases_by_module(modules: dict[str, Module]) -> dict[str, tuple[str, ...]]:
    return {name: module.aliases for name, module in modules.items()}


def resolve_modules(selected: set[str], modules: dict[str, Module]) -> tuple[list[str], set[str]]:
    resolved = set(selected)
    added = set()
    changed = True

    while changed:
        changed = False
        for name in tuple(resolved):
            for dependency in modules[name].dependencies:
                if dependency not in modules:
                    raise ValueError(f"module {name!r} depends on unknown module {dependency!r}")
                if dependency not in resolved:
                    resolved.add(dependency)
                    added.add(dependency)
                    changed = True

    return [name for name in MODULE_ORDER if name in resolved], added
