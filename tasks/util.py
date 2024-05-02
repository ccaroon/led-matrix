import os
import shutil

ROOT_DIR = os.path.abspath(f"{os.path.basename(__file__)}/..")

USER = os.environ.get("USER")
DEVICE_DEST = f"/media/{USER}/CIRCUITPY"


# -- FOR TESTING --
# DEVICE_DEST = f"/tmp/{USER}/CIRCUITPY"


def install_project(src_code):
    # Install Module
    cp_tree(
        src_code["module"],
        f"{DEVICE_DEST}",
        ignore=src_code.get("ignore", [])
    )

    # Install Main
    cp_if_newer(src_code["main"], f"{DEVICE_DEST}/main.py")

    # Install Libs
    for file in src_code["libs"]:
        src = f"lib/{file}"
        dest_dir = f"{DEVICE_DEST}/lib"
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


def read_requirements(file):
    reqs = []
    with open(file, "r") as fptr:
        line = fptr.readline().strip()
        while line:
            if not line.startswith("#"):
                reqs.append(line)
            line = fptr.readline().strip()
    return reqs
    
