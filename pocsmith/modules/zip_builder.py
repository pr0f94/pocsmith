from .base import Module


MODULE = Module(
    name="zip_builder",
    aliases=("zip-builder",),
    imports=("import io", "import zipfile"),
    functions=(
        'def build_zip(entries):\n    # entries: {"path/in/archive.txt": b"content"}\n    buffer = io.BytesIO()\n    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:\n        for archive_path, content in entries.items():\n            archive.writestr(archive_path, content)\n    buffer.seek(0)\n    return buffer.getvalue()',
    ),
)
