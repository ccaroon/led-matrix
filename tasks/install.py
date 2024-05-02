import os
import shutil
import zipfile

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
def playground(ctx):
    """ Install the Playground project """
    src_code = {
        "module": "playground",
        "main": "playground/main.py",
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
def boids(ctx):
    """ Install the Boids project """

    src_code = {
        "module": "boids",
        "main": "boids/main.py",
        "libs": [
            "led_matrix.py"
        ],
        "ignore": [
            "README.md"
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



BUNDLES = {
    "Adafruit_CircuitPython_Bundle": {
        "prefix": "adafruit-circuitpython-bundle",
        "version": ("8", "20240501")
    },
    "CircuitPython_Community_Bundle": {
        "prefix": "circuitpython-community-bundle",
        "version": ("8", "20240502")
    }
}
@task
def requirements(ctx, reqs_file):
    """ Install CircuitPython Requirements """
    
    # Make download dir
    download_dir = f"{util.ROOT_DIR}/.circuit-python"
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
    reqs = util.read_requirements(reqs_file)
    for req in reqs:
        bundle_name = os.path.dirname(req) or "Adafruit_CircuitPython_Bundle"
        bundle = BUNDLES.get(bundle_name)
        bundle_prefix = bundle["prefix"]
        bundle_version = bundle["version"]
        bundle_dir = f"{bundle_prefix}-{bundle_version[0]}.x-mpy-{bundle_version[1]}"
        
        pkg_name = os.path.basename(req)

        src = f"{download_dir}/{bundle_dir}/lib/{pkg_name}"
        dst = f"{util.DEVICE_DEST}/lib"
        if os.path.isfile(src):
            util.cp_if_newer(src, f"{dst}/{pkg_name}")
        elif os.path.isdir(src):
            util.cp_tree(src, dst)
