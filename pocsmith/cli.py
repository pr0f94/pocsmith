from __future__ import annotations

import argparse
import os
from importlib import resources
from pathlib import Path
import sys

try:
    import yaml
except ModuleNotFoundError:
    yaml = None

from pocsmith.builder import ExploitBuilder
from pocsmith.registry import alias_map, aliases_by_module, load_modules, resolve_modules


ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "cyan": "\033[36m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "dim": "\033[2m",
}


def should_color(argv: list[str] | None = None, stream=sys.stdout) -> bool:
    argv = argv or []
    if "--no-color" in argv:
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    if os.environ.get("NO_COLOR"):
        return False
    return stream.isatty()


def color(text: str, style: str, enabled: bool) -> str:
    if not enabled:
        return text
    return f"{ANSI[style]}{text}{ANSI['reset']}"


class PocsmithArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, profiles: dict[str, list[str]] | None = None, color_enabled: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self._profiles = profiles or {}
        self._color_enabled = color_enabled

    def format_help(self) -> str:
        help_text = self._color_help(super().format_help().rstrip())
        if not self._profiles:
            return help_text + "\n"

        lines = [help_text, "", color("profiles:", "bold", self._color_enabled)]
        for profile in sorted(self._profiles):
            lines.append(f"  {color(profile, 'green', self._color_enabled)}")
        return "\n".join(lines) + "\n"

    def _color_help(self, help_text: str) -> str:
        if not self._color_enabled:
            return help_text

        colored_lines = []
        for line in help_text.splitlines():
            stripped = line.strip()
            if stripped in {"usage:", "optional arguments:", "options:", "module aliases:"}:
                colored_lines.append(line.replace(stripped, color(stripped, "bold", True), 1))
                continue
            if stripped.startswith("--") or stripped.startswith("-"):
                indent = line[: len(line) - len(line.lstrip())]
                parts = line.strip().split(maxsplit=1)
                flag_text = parts[0]
                rest = f" {parts[1]}" if len(parts) > 1 else ""
                colored_lines.append(f"{indent}{color(flag_text, 'cyan', True)}{rest}")
                continue
            colored_lines.append(line)
        return "\n".join(colored_lines)


PROFILE_RESOURCE = "profiles.yaml"


def _load_profiles_without_pyyaml(text: str) -> dict[str, list[str]]:
    profiles: dict[str, list[str]] = {}
    current = None

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.split("#", 1)[0].rstrip()
        if not line:
            continue
        if not line.startswith(" ") and line.endswith(":"):
            current = line[:-1].strip()
            if not current:
                raise ValueError(f"invalid empty profile name on line {line_number}")
            profiles[current] = []
            continue
        if line.startswith("  - ") and current:
            profiles[current].append(line[4:].strip())
            continue
        raise ValueError(f"unsupported profiles.yaml syntax on line {line_number}: {raw_line}")

    return profiles


def load_profiles(resource_name: str = PROFILE_RESOURCE) -> dict[str, list[str]]:
    try:
        text = resources.files("pocsmith").joinpath(resource_name).read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}

    data = yaml.safe_load(text) if yaml else _load_profiles_without_pyyaml(text)
    data = data or {}
    if not isinstance(data, dict):
        raise ValueError(f"{resource_name} must contain a mapping of profile names to alias lists")

    profiles = {}
    for name, aliases in data.items():
        if not isinstance(name, str) or not isinstance(aliases, list) or not all(isinstance(alias, str) for alias in aliases):
            raise ValueError(f"profile {name!r} must be a list of alias names")
        profiles[name] = aliases
    return profiles


def build_parser(module_aliases: dict[str, str], profiles: dict[str, list[str]], color_enabled: bool) -> argparse.ArgumentParser:
    parser = PocsmithArgumentParser(
        description="Generate modular Python exploit templates",
        profiles=profiles,
        color_enabled=color_enabled,
        add_help=False,
    )
    parser.add_argument("-h", "--help", action="store_true", help="show this help message and exit")
    parser.add_argument("-o", "--output", required=True, help="Output exploit file")
    parser.add_argument("--force", action="store_true", help="Overwrite output file if it already exists")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("--profile", metavar="PROFILE", help="Load aliases from profiles.yaml")

    alias_group = parser.add_argument_group("module aliases")
    for alias in sorted(module_aliases):
        alias_group.add_argument(f"--{alias}", action="store_true", dest=alias.replace("-", "_"))

    return parser


def selected_aliases(args: argparse.Namespace, module_aliases: dict[str, str], profiles: dict[str, list[str]]) -> list[str]:
    selected = []
    if args.profile:
        selected.extend(profiles[args.profile])

    for alias in sorted(module_aliases):
        if getattr(args, alias.replace("-", "_")):
            selected.append(alias)

    return selected


def run(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    color_enabled = should_color(argv)
    modules = load_modules()
    module_aliases = alias_map(modules)
    profiles = load_profiles()
    parser = build_parser(module_aliases, profiles, color_enabled)
    if "-h" in argv or "--help" in argv:
        print(parser.format_help(), end="")
        return 0

    args = parser.parse_args(argv)
    color_enabled = color_enabled and not args.no_color

    if args.profile and args.profile not in profiles:
        parser.error(f"unknown profile: {args.profile}")

    aliases = selected_aliases(args, module_aliases, profiles)
    if not aliases:
        parser.error("select at least one module alias or --profile")

    unknown_aliases = sorted({alias for alias in aliases if alias not in module_aliases})
    if unknown_aliases:
        parser.error(f"unknown aliases in profile: {', '.join(unknown_aliases)}")

    selected_modules = {module_aliases[alias] for alias in aliases}
    ordered_names, added = resolve_modules(selected_modules, modules)
    ordered_modules = [modules[name] for name in ordered_names]
    module_aliases_by_name = aliases_by_module(modules)

    output = Path(args.output)
    if output.exists() and not args.force:
        parser.error(f"{output} already exists; use --force to overwrite")

    output.write_text(ExploitBuilder(ordered_modules).build(), encoding="utf-8")

    selected_alias_text = ", ".join(dict.fromkeys(aliases))
    added_aliases = [alias for name in ordered_names if name in added for alias in module_aliases_by_name[name]]
    added_text = ", ".join(added_aliases) or "none"
    print(f"{color('Selected aliases:', 'bold', color_enabled)} {color(selected_alias_text, 'cyan', color_enabled)}")
    print(f"{color('Added dependencies:', 'bold', color_enabled)} {color(added_text, 'yellow', color_enabled)}")
    print(f"{color('Wrote:', 'bold', color_enabled)} {color(str(output), 'green', color_enabled)}")
    return 0


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
