from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RuntimeArg:
    flags: tuple[str, ...]
    kwargs: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class Module:
    name: str
    aliases: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    imports: tuple[str, ...] = ()
    runtime_args: tuple[RuntimeArg, ...] = ()
    globals: tuple[str, ...] = ()
    main_setup: tuple[str, ...] = ()
    functions: tuple[str, ...] = ()
    startup: tuple[str, ...] = ()
    main_body: tuple[str, ...] = ()
