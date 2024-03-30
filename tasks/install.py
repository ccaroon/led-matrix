import os
import shutil
from invoke import task

import util


@task
def settings(ctx):
    """ Install settings.toml """
    util.cp_if_newer("settings.toml", f"{util.BASE_DEST}/settings.toml")


@task
def main(ctx, file):
    """
    Always copy given file as `main.py`

    Args:
        file (str): Path of file to install as `main.py`
    """
    print(f"==> {file}")
    shutil.copy(file, f"{util.BASE_DEST}/main.py")


@task
def file(ctx, file):
    """
    Copy given file to device

    Args:
        file (str): Path of the file to copy
    """
    util.cp_if_newer(file, f"{util.BASE_DEST}/{file}")


@task(settings)
def playground(ctx):
    """ Install the Playground project """
    src_code = {
        "module": "playground",
        "main":   "playground/main.py",
        "libs": [
            "led_matrix.py"
        ]
    }

    util.install_project(src_code)


@task(pre=[settings], aliases=["gol"])
def game_of_life(ctx):
    """ Install the Game Of Life project """

    src_code = {
        "module": "game_of_life",
        "main": "game_of_life/main.py",
        "libs": [
            "led_matrix.py"
        ]
    }

    util.install_project(src_code)


@task(settings)
def info_panel(ctx):
    """ Install the InfoPanel project """

    src_code = {
        "module": "info_panel",
        "main": "info_panel/main.py",
        "libs": [
            "colors",
            "aio.py",
            "chronos.py",
            "led_matrix.py",
            "my_wifi.py"
        ]
    }

    util.install_project(src_code)


@task
def clean(ctx, project=None):
    """ Remove / Cleanup currently install project """

    # files
    for file in ("main.py", "settings.toml"):
        path = f"{util.BASE_DEST}/{file}"
        if os.path.exists(path):
            print(f"==> Removing {path} ...")
            os.remove(path)

    # lib
    lib_path = f"{util.BASE_DEST}/lib"
    if os.path.exists(lib_path):
        print(f"==> Removing {lib_path} ...")
        shutil.rmtree(lib_path, onexc=util.not_found)

    # project
    if project is not None:
        prj_path = f"{util.BASE_DEST}/{project}"
        if os.path.exists(prj_path):
            print(f"==> Removing {prj_path} ...")
            shutil.rmtree(prj_path, onexc=util.not_found)
