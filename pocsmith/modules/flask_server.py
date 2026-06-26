from .base import Module, RuntimeArg


MODULE = Module(
    name="flask_server",
    aliases=("flask",),
    imports=(
        "import threading",
        "import time",
        "from flask import Flask, request",
    ),
    runtime_args=(
        RuntimeArg(("--callback-ip",), {"required": True, "help": "Local callback/listener IP"}),
        RuntimeArg(("--flask-port",), {"required": True, "type": int, "help": "Local Flask callback port"}),
    ),
    globals=(
        "app = Flask(__name__)",
    ),
    main_setup=(
        'callback_url = f"http://{args.callback_ip}:{args.flask_port}"',
    ),
    functions=(
        '''def start_flask(args):
    thread = threading.Thread(
        target=lambda: app.run(host=args.callback_ip, port=args.flask_port, debug=False, use_reloader=False),
        daemon=True,
    )
    thread.start()
    time.sleep(1)
    return thread''',
    ),
    startup=("start_flask(args)",),
)
