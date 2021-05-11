import os
import subprocess
import time

from common import (
    cmd_common,
    dist_folder,
    main_gui_py,
    main_py,
    matplotlibrc,
    shutil_copy_verbose,
    src_folder,
)


def main():

    time.time()

    os.chdir(src_folder)

    if not matplotlibrc.is_file():
        raise RuntimeError(f'Could not find: "{matplotlibrc}"')

    # gui
    cmd = cmd_common + ["-w", str(main_gui_py)]
    gui_start_time = time.time()
    subprocess.call(cmd, shell=True)
    shutil_copy_verbose(
        matplotlibrc, dist_folder / main_py.name.replace(main_py.suffix, "")
    )
    gui_time = time.time() - gui_start_time
    print(f"\nGUI build time: {int(gui_time//60)} min {int(gui_time%60)} sec")


if __name__ == "__main__":
    main()
