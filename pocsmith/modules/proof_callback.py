from .base import Module


MODULE = Module(
    name="proof_callback",
    aliases=("proof",),
    dependencies=("callback_value_handler",),
    functions=(
        '@app.route("/proof")\ndef on_proof():\n    return callback_value("proof.txt")',
    ),
)
