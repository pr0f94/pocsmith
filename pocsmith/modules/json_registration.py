from .base import Module


MODULE = Module(
    name="json_registration",
    aliases=("register-json",),
    dependencies=("requests_session",),
    functions=(
        '''def register_json(session, base_url, username, password):
    # TODO: update registration path and JSON keys.
    response = session.post(
        f"{base_url}/register",
        json={"username": username, "password": password},
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return response''',
    ),
)
