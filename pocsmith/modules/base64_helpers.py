from .base import Module


MODULE = Module(
    name="base64_helpers",
    aliases=("base64",),
    imports=("import base64",),
    functions=(
        'def b64e(data):\n    if isinstance(data, str):\n        data = data.encode()\n    return base64.b64encode(data).decode("ascii")\n\n\ndef b64d(data):\n    return base64.b64decode(data)',
    ),
)
