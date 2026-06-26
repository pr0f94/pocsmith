from .base import Module


MODULE = Module(
    name="cookie_callback",
    aliases=("cookie",),
    dependencies=("flask_server", "queue_state"),
    functions=(
        '''@app.route("/cookie")
def on_cookie():
    cookie = request.args.get("cookie", "")
    q.put(cookie)
    print(f"cookie: {cookie}")
    return ""''',
    ),
)
