from .base import Module, RuntimeArg


MODULE = Module(
    name="netcat_listener",
    aliases=("netcat",),
    imports=("import subprocess",),
    runtime_args=(
        RuntimeArg(("--nc-port",), {"required": True, "type": int, "help": "Local netcat listener port"}),
    ),
    functions=(
        '''def start_netcat(args):
    return subprocess.Popen(["nc", "-lvnp", str(args.nc_port)])''',
    ),
    startup=("nc_process = start_netcat(args)",),
)
