import os
import shutil
import yaml

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


@task(settings)
def project(ctx, project_path):
    """ Install the named Project and Dependencies """
    with open(project_path, "r") as fptr:
        project_data = yaml.safe_load(fptr)

    util.install_project(ctx, project_data)


@task
def clean(ctx, project=None):
    """ Remove / Cleanup currently install project """

    # files
    for file in ("main.py", "settings.toml"):
        path = f"{util.DEVICE_DEST}/{file}"
        if os.path.exists(path):
            print(f"==> Removing {path} ...")
            os.remove(path)

    # lib
    lib_path = f"{util.DEVICE_DEST}/lib"
    if os.path.exists(lib_path):
        print(f"==> Removing {lib_path} ...")
        shutil.rmtree(lib_path, onexc=util.not_found)

    # project
    if project is not None:
        prj_path = f"{util.DEVICE_DEST}/{project}"
        if os.path.exists(prj_path):
            print(f"==> Removing {prj_path} ...")
            shutil.rmtree(prj_path, onexc=util.not_found)


@task(aliases=["list"])
def view(ctx):
    """ View / List the contents of the device """
    if shutil.which("tree"):
        ctx.run(f"tree {util.DEVICE_DEST}")
    else:
        ctx.run(f"ls -1FR {util.DEVICE_DEST}")
