from .base import Module


MODULE = Module(
    name="csrf",
    aliases=("csrf",),
    dependencies=("requests_session", "html_parser"),
    functions=(
        'def fetch_csrf_token(session, base_url, path, field_name="csrf"):\n    # TODO: update path and field name for the target app.\n    response = session.get(f"{base_url}{path}")\n    response.raise_for_status()\n    soup = parse_html(response)\n    token = find_input_value(soup, field_name)\n    if token is None:\n        raise ValueError(f"could not find CSRF field: {field_name}")\n    return token',
    ),
)
