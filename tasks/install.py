import os
import shutil

from invoke import task

import util


@task
def settings(ctx):
    """ Install settings.toml """
    util.cp_if_newer("settings.toml", f"{util.DEVICE_DEST}/settings.toml")


@task
def main(ctx, file):
    """
    Always copy given file as `main.py`

    Args:
        file (str): Path of file to install as `main.py`
    """
    print(f"==> {file}")
    shutil.copy(file, f"{util.DEVICE_DEST}/main.py")


@task
def file(ctx, file):
    """
    Copy given file to device

    Args:
        file (str): Path of the file to copy
    """
    util.cp_if_newer(file, f"{util.DEVICE_DEST}/{file}")


@task(
    pre=[settings],
    help={
        "path": "Path to project directory or project.yml file."
    }
)
def project(ctx, path):
    """ Install the named Project and Dependencies """
    project_data = util.load_project(path)
    util.install_project(ctx, project_data)


@task(iterable=["package"])
def clean(ctx, package=None):
    """
    Remove files from device.

    if `package` is None, only clean basic files.
    """

    # Basic files
    for file in ("main.py", "settings.toml"):
        path = f"{util.DEVICE_DEST}/{file}"
        if os.path.exists(path):
            print(f"==> Removing {path} ...")
            os.remove(path)

    # `lib` dir - includes "libs" & "requirements"
    lib_path = f"{util.DEVICE_DEST}/lib"
    if os.path.exists(lib_path):
        print(f"==> Removing {lib_path} ...")
        shutil.rmtree(lib_path, onexc=util.not_found)

    # Any packages
    for pkg in package:
        pkg_path = f"{util.DEVICE_DEST}/{pkg}"
        if os.path.exists(pkg_path):
            print(f"==> Removing {pkg_path} ...")
            shutil.rmtree(pkg_path, onexc=util.not_found)


@task(aliases=["list"])
def view(ctx):
    """ View / List the contents of the device """
    if shutil.which("tree"):
        ctx.run(f"tree {util.DEVICE_DEST}")
    else:
        ctx.run(f"ls -1FR {util.DEVICE_DEST}")
