import os
import shutil
import zipfile

ROOT_DIR = os.path.abspath(f"{os.path.basename(__file__)}/..")

USER = os.environ.get("USER")

# Development System Setup
__DEV_OS = "linux"

__DEVICES = {
    "test": f"/tmp/{USER}/CIRCUITPY",
    "linux": f"/media/{USER}/CIRCUITPY",
    "mac": "/Volumes/CIRCUITPY"
}
DEVICE_DEST = __DEVICES[__DEV_OS]

__PORTS = {
    "linux": "/dev/ttyACM0",
    "mac": "/dev/tty.usbmodem84722E93560F1"
}
SHELL_PORT = __PORTS[__DEV_OS]

# CircuitPython Library Bundles
BUNDLES = {
    "Adafruit_CircuitPython_Bundle": {
        "prefix": "adafruit-circuitpython-bundle",
        "version": ("9", "20240503")
    },
    "CircuitPython_Community_Bundle": {
        "prefix": "circuitpython-community-bundle",
        "version": ("9", "20240502")
    }
}


def install_project(ctx, prj_data):
    # Install Module
    cp_tree(
        prj_data["module"],
        f"{DEVICE_DEST}",
        ignore=prj_data.get("ignore", [])
    )

    # Install Main
    cp_if_newer(prj_data["main"], f"{DEVICE_DEST}/main.py")

    # Install Libs
    for file in prj_data["libs"]:
        src = f"lib/{file}"
        dest_dir = f"{DEVICE_DEST}/lib"
        if os.path.isdir(src):
            cp_tree(src, dest_dir)
        else:
            cp_if_newer(src, f"{dest_dir}/{file}")

    # Install requirements
    if prj_data["requirements"]:
        install_requirements(ctx, prj_data["requirements"])


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


# TODO: Allow `requirements` section to override CPY & Bundle Versions
def install_requirements(ctx, reqs_list):
    """ Install CircuitPython Requirements """
    
    # Make download dir
    download_dir = f"{ROOT_DIR}/.circuit-python"
    os.makedirs(download_dir, exist_ok=True)
    
    for bundle_name, bundle in BUNDLES.items():
        prefix = bundle["prefix"]
        cpy_version = bundle["version"][0]
        bnd_version = bundle["version"][1]
        # Download libs from cpy site if not exist
        zip_file = f"{prefix}-{cpy_version}.x-mpy-{bnd_version}.zip"
        if not os.path.exists(f"{download_dir}/{zip_file}"):
            print(f"=> Downloading {zip_file}...")
            with ctx.cd(download_dir):
                ctx.run(f"wget -q https://github.com/adafruit/{bundle_name}/releases/download/{bnd_version}/{zip_file}")

            # unzip
            print(f"=> Extracting {zip_file}...")
            with zipfile.ZipFile(f"{download_dir}/{zip_file}", 'r') as ziptr:
                ziptr.extractall(path=download_dir)

    # cp reqs to device
    for req in reqs_list:
        bundle_name = os.path.dirname(req) or "Adafruit_CircuitPython_Bundle"
        bundle = BUNDLES.get(bundle_name)
        bundle_prefix = bundle["prefix"]
        bundle_version = bundle["version"]
        bundle_dir = f"{bundle_prefix}-{bundle_version[0]}.x-mpy-{bundle_version[1]}"
        
        pkg_name = os.path.basename(req)

        src = f"{download_dir}/{bundle_dir}/lib/{pkg_name}"
        dst = f"{DEVICE_DEST}/lib"
        if os.path.isfile(src):
            cp_if_newer(src, f"{dst}/{pkg_name}")
        elif os.path.isdir(src):
            cp_tree(src, dst)
        else:
            print(f"WARNING: Cant' find: {src}")





# 
