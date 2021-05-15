import os
import shutil
import subprocess
import time

from common import *


def shutil_copy_verbose(src: str, dst: str) -> None:
    print(f'Copying "{src}" to "{dst}"')
    shutil.copy(src, dst)


def buildPyInstaller():
    start_time = time.time()

    hidden_imports = [
        "uvicorn.logging",
        "uvicorn.loops",
        "uvicorn.loops.auto",
        "uvicorn.protocols",
        "uvicorn.protocols.http",
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.websockets",
        "uvicorn.protocols.websockets.auto",
        "uvicorn.lifespan",
        "uvicorn.lifespan.on",
    ]

    hidden_matplotlib = [
        "matplotlib.backends.backend_svg",
        "matplotlib.backends.backend_tkagg",
    ]
    hidden_imports = hidden_imports + hidden_matplotlib

    cmd_options = ["--clean", "--onedir", "--console"]

    for i in hidden_imports:
        cmd_options.append("--hidden-import")
        cmd_options.append(i)

    cmd = [python_exe, "-m", "PyInstaller"] + cmd_options + [main_py]

    subprocess.call(cmd, shell=True)
    shutil_copy_verbose(
        matplotlibrc,
        os.path.join(dist_folder, os.path.splitext(os.path.basename(main_py))[0]),
    )
    shutil_copy_verbose(matplotlibrc, dist_folder)
    shutil.copytree(mpl_data_dir, mpl_destination, dirs_exist_ok=True)

    # copy to UI folder if...
    if os.path.isdir(ui_folder):
        print("Copying to " + ui_folder)
        shutil.copytree(
            os.path.join(dist_folder, "local_api"),
            os.path.join(ui_folder, "msanalyzer_api"),
            dirs_exist_ok=True,
        )

    elapsed_time = time.time() - start_time

    if elapsed_time > 60.0:
        print(
            f"\nPyInstaller elapsed time: {int(elapsed_time//60)}min{elapsed_time%60:.2f}seconds"
        )
    else:
        print(f"\nPyInstaller elapsed time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    buildPyInstaller()
