from .base import Module


MODULE = Module(
    name="regex_extract",
    aliases=("regex-extract",),
    imports=("import re",),
    functions=(
        'def regex_extract(pattern, text, group=1, flags=0):\n    # TODO: update pattern and group number.\n    match = re.search(pattern, text, flags)\n    if not match:\n        raise ValueError("pattern not found")\n    return match.group(group)',
    ),
)
