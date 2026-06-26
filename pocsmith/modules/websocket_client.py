from .base import Module


MODULE = Module(
    name="websocket_client",
    aliases=("websocket",),
    dependencies=("requests_session",),
    imports=("from websocket import create_connection",),
    functions=(
        '''def websocket_connect(args, path):
    scheme = "wss" if args.https else "ws"
    url = f"{scheme}://{args.target}{path}"
    return create_connection(url)''',
    ),
)
