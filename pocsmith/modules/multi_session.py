from .base import Module


MODULE = Module(
    name="multi_session",
    aliases=("multi-session",),
    dependencies=("requests_session",),
    main_setup=(
        "admin_session = requests.Session()",
    ),
)
