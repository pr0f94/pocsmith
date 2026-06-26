from .base import Module


MODULE = Module(
    name="json_auth",
    aliases=("auth-json",),
    dependencies=("requests_session",),
    functions=(
        '''def login_json(session, base_url, username, password):
    # TODO: update login path and JSON keys.
    response = session.post(
        f"{base_url}/login",
        json={"username": username, "password": password},
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return response''',
    ),
)
