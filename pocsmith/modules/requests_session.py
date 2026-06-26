from .base import Module, RuntimeArg


MODULE = Module(
    name="requests_session",
    aliases=("session",),
    imports=("import requests",),
    runtime_args=(
        RuntimeArg(("--target",), {"required": True, "help": "Target host[:port], without scheme"}),
        RuntimeArg(("--https",), {"action": "store_true", "help": "Use HTTPS for target requests"}),
    ),
    main_setup=(
        'scheme = "https" if args.https else "http"',
        'base_url = f"{scheme}://{args.target}"',
        "session = requests.Session()",
    ),
)
