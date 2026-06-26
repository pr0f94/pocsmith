from .base import Module


MODULE = Module(
    name="headers",
    aliases=("headers",),
    dependencies=("requests_session",),
    functions=(
        'def set_bearer_header(session, token, header="Authorization"):\n    session.headers.update({header: f"Bearer {token}"})\n\n\ndef set_cookie_header(session, cookie):\n    session.headers.update({"Cookie": cookie})\n\n\ndef set_origin_headers(session, base_url):\n    session.headers.update({"Origin": base_url, "Referer": f"{base_url}/"})\n\n\ndef merge_headers(*headers):\n    merged = {}\n    for header_set in headers:\n        merged.update(header_set)\n    return merged',
    ),
)
