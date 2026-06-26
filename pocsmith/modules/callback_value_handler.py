from .base import Module


MODULE = Module(
    name="callback_value_handler",
    dependencies=("flask_server",),
    functions=(
        'def callback_value(label, param="flag"):\n    value = request.args.get(param, "")\n    print(f"{label}: {value}")\n    return ""',
    ),
)
