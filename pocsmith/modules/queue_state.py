from .base import Module


MODULE = Module(
    name="queue_state",
    imports=("import queue",),
    globals=("q = queue.Queue()",),
)
