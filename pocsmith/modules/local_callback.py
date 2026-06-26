from .base import Module


MODULE = Module(
    name="local_callback",
    aliases=("local",),
    dependencies=("callback_value_handler",),
    functions=(
        '@app.route("/local")\ndef on_local():\n    return callback_value("local.txt")',
    ),
)
