from .base import Module


MODULE = Module(
    name="form_auth",
    aliases=("auth-form",),
    dependencies=("requests_session",),
    functions=(
        '''def login_form(session, base_url, username, password):
    # TODO: update login path and parameter names.
    response = session.post(
        f"{base_url}/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    return response''',
    ),
)
