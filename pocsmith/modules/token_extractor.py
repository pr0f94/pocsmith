from .base import Module


MODULE = Module(
    name="token_extractor",
    aliases=("token-extractor",),
    functions=(
        'def extract_json_value(response, key):\n    # TODO: set the JSON key to extract.\n    return response.json()[key]\n\n\ndef extract_cookie_value(response, name):\n    # TODO: set the cookie name to extract.\n    return response.cookies.get(name)\n\n\ndef extract_header_value(response, name):\n    # TODO: set the header name to extract.\n    return response.headers.get(name)',
    ),
)
