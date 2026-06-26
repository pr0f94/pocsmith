from __future__ import annotations

from collections.abc import Iterable

from pocsmith.modules.base import Module, RuntimeArg


def _dedupe(items: Iterable[str]) -> list[str]:
    seen = set()
    deduped = []
    for item in items:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def _indent(block: str, spaces: int = 4) -> str:
    prefix = " " * spaces
    return "\n".join(f"{prefix}{line}" if line else "" for line in block.splitlines())


class ExploitBuilder:
    def __init__(self, modules: list[Module]) -> None:
        self.modules = modules

    def build(self) -> str:
        imports = self._imports()
        top_level_globals = self._globals()
        parser_args = self._parser_args()
        main_setup = self._main_setup()
        functions = self._functions()
        startup = self._startup()
        main_body = self._main_body()

        sections = [
            imports,
            top_level_globals,
            self._parse_args_function(parser_args),
            functions,
            self._main_function(main_setup, startup, main_body),
            'if __name__ == "__main__":\n    main()',
        ]
        return "\n\n\n".join(section for section in sections if section).rstrip() + "\n"

    def _imports(self) -> str:
        imports = ["import argparse"]
        for module in self.modules:
            imports.extend(module.imports)
        return "\n".join(_dedupe(imports))

    def _runtime_args(self) -> list[RuntimeArg]:
        args = []
        seen = set()
        for module in self.modules:
            for runtime_arg in module.runtime_args:
                key = runtime_arg.flags
                if key not in seen:
                    seen.add(key)
                    args.append(runtime_arg)
        return args

    def _parser_args(self) -> list[str]:
        lines = []
        for runtime_arg in self._runtime_args():
            flags = ", ".join(repr(flag) for flag in runtime_arg.flags)
            kwargs = ", ".join(f"{key}={self._render_kwarg(value)}" for key, value in runtime_arg.kwargs.items())
            if kwargs:
                lines.append(f"parser.add_argument({flags}, {kwargs})")
            else:
                lines.append(f"parser.add_argument({flags})")
        return lines

    def _render_kwarg(self, value: object) -> str:
        if value is int:
            return "int"
        if value is str:
            return "str"
        return repr(value)

    def _parse_args_function(self, parser_args: list[str]) -> str:
        lines = [
            "def parse_args():",
            '    parser = argparse.ArgumentParser(description="Generated exploit template")',
        ]
        lines.extend(f"    {line}" for line in parser_args)
        lines.append("    return parser.parse_args()")
        return "\n".join(lines)

    def _globals(self) -> str:
        lines = []
        for module in self.modules:
            lines.extend(module.globals)
        return "\n".join(lines)

    def _main_setup(self) -> list[str]:
        lines = []
        for module in self.modules:
            lines.extend(module.main_setup)
        return lines

    def _functions(self) -> str:
        blocks = []
        for module in self.modules:
            blocks.extend(module.functions)
        return "\n\n\n".join(blocks)

    def _startup(self) -> list[str]:
        lines = []
        for module in self.modules:
            lines.extend(module.startup)
        return lines

    def _main_body(self) -> list[str]:
        lines = []
        for module in self.modules:
            lines.extend(module.main_body)
        lines.extend(
            [
                "# TODO: add exploit chain here.",
                "pass",
            ]
        )
        return lines

    def _main_function(self, main_setup: list[str], startup: list[str], main_body: list[str]) -> str:
        lines = ["def main():", "    args = parse_args()"]
        lines.extend(_indent(line) for line in main_setup)
        lines.extend(_indent(line) for line in startup)
        lines.extend(_indent(line) for line in main_body)
        return "\n".join(lines)
