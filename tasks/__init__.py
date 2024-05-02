import shutil
import os
from invoke import Collection, task

import install
import util

MAC_PORT = "/dev/tty.SLAB_USBtoUART"
LNX_PORT = "/dev/ttyACM0"


@task
def shell(ctx, port=LNX_PORT):
    """ Use picocom to run the REPL """

    # NOTE: doesn't behave properly with run()...even with pty=True
    # ctx.run(f"picocom {port} -b115200", pty=True)
    os.execlp("picocom",  ".", port, "-b115200")

@task
def clean(ctx):
    """ Clean Stuff """
    # .circuit-python
    cpy_path = f"{util.ROOT_DIR}/.circuit-python"
    if os.path.exists(cpy_path):
        print(f"==> Removing {cpy_path} ...")
        shutil.rmtree(cpy_path, onexc=util.not_found)

namespace = Collection(
    clean,
    shell,
    install
)
