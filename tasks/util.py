import os
import shutil

USER = os.environ.get("USER")
BASE_DEST = f"/media/{USER}/CIRCUITPY"


# -- FOR TESTING --
# BASE_DEST = f"/tmp/{USER}/CIRCUITPY"


def install_project(src_code):
    # Install Module
    cp_tree(
        src_code["module"],
        f"{BASE_DEST}",
        ignore=src_code.get("ignore", [])
    )

    # Install Main
    cp_if_newer(src_code["main"], f"{BASE_DEST}/main.py")

    # Install Libs
    for file in src_code["libs"]:
        src = f"lib/{file}"
        dest_dir = f"{BASE_DEST}/lib"
        if os.path.isdir(src):
            cp_tree(src, dest_dir)
        else:
            cp_if_newer(src, f"{dest_dir}/{file}")


def cp_tree(src, dest, **kwargs):
    """
    Copy files from a src directory to a dest directory.

    Args:
        src (str): Source Directory
        dest (str: Destination Directory
    """
    shutil.copytree(
        src,
        f"{dest}/{os.path.basename(src)}",
        copy_function=cp_if_newer,
        ignore=lambda src_dir, names: kwargs.get("ignore", []),
        dirs_exist_ok=True
    )


def cp_if_newer(src, dest):
    """
    Copy src to dest, but only if src is newer than dest.

    Args:
        src (str): Full path of src file
        dest (str): Full path of dest file
    """
    if not os.path.exists(dest) or is_newer(src, dest):
        print(f"==> {src} -> {dest}...")
        dst_path = os.path.dirname(dest)
        os.makedirs(dst_path, exist_ok=True)
        shutil.copy(src, dest)


def is_newer(file1, file2):
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


def not_found(func, path, exc_info):
    print(f"=> {path} ... Nothing to do!")
