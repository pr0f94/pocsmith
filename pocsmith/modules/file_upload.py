from .base import Module


MODULE = Module(
    name="file_upload",
    aliases=("file-upload",),
    dependencies=("requests_session",),
    functions=(
        'def upload_file(session, base_url, path, field_name, filename, content, content_type="application/octet-stream", data=None, headers=None):\n    # TODO: update path, field name, extra form data, and headers.\n    files = {field_name: (filename, content, content_type)}\n    response = session.post(f"{base_url}{path}", files=files, data=data or {}, headers=headers or {})\n    response.raise_for_status()\n    return response',
    ),
)
