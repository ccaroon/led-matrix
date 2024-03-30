from invoke import Collection, task

import install

MAC_PORT = "/dev/tty.SLAB_USBtoUART"
LNX_PORT = "/dev/ttyACM0"


@task
def shell(ctx, port=LNX_PORT):
    """ Use picocom to run the REPL """
    ctx.run(f"picocom {port} -b115200")


namespace = Collection(
    shell,
    install
)
