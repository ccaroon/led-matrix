import os
# import pathlib
import shutil

from invoke import task

USER = os.environ.get("USER")
# BASE_DEST = f"/media/{USER}/CIRCUITPY"
BASE_DEST = f"/tmp/{USER}/CIRCUITPY"


@task
def playground(ctx):
    # `dest` is relative to BASE_DEST
    src_code = (
        {"src": "playground/main.py", "dest": "/"},
        {"src": "lib/led_matrix.py", "dest": "/lib"}

    )

    for file in src_code:
        src = file["src"]
        src_name = os.path.basename(src)
        dest = f"{BASE_DEST}{file["dest"]}/{src_name}"
        __cp_if_newer(src, dest)


# with ctx.cd(__docs_dir()):
#     ctx.run("sphinx-build -M html . _build")

#
# Helper functions
#


def __cp_tree(src, dest):
    """
    Copy files from a src directory to a dest directory.

    Args:
        src (str): Source Directory
        dest (str: Destination Directory
    """
    shutil.copytree(src, dest, copy_function=__cp_if_newer, dirs_exist_ok=True)


def __cp_if_newer(src, dest):
    """
    Copy src to dest, but only if src is newer than dest.

    Args:
        src (str): Full path of src file
        dest (str): Full path of dest file
    """
    if not os.path.exists(dest) or __is_newer(src, dest):
        print(f"==> {src} -> {dest}...")
        dst_path = os.path.dirname(dest)
        os.makedirs(dst_path, exist_ok=True)
        shutil.copy(src, dest)


def __is_newer(file1, file2):
    """
    Is `file1` newer than `file2`?

    Args:
        file1 (str): Path to a file
        file2 (str): Path to a file

    Returns:
        boolean: True if file1 is newer than file2, False otherwise
    """
    mt1 = os.path.getmtime(file1)
    mt2 = os.path.getmtime(file2)

    return mt1 > mt2
