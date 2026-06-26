from .base import Module


MODULE = Module(
    name="websocket_async",
    aliases=("websocket-async",),
    dependencies=("requests_session",),
    imports=("import asyncio", "import websockets"),
    functions=(
        'async def websocket_async_connect(args, path):\n    scheme = "wss" if args.https else "ws"\n    url = f"{scheme}://{args.target}{path}"\n    return await websockets.connect(url)\n\n\nasync def websocket_send_recv(args, path, message):\n    # TODO: update path and message format.\n    async with await websocket_async_connect(args, path) as websocket:\n        await websocket.send(message)\n        return await websocket.recv()',
    ),
)
