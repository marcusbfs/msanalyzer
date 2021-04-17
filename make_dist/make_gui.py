import os
import subprocess
import shutil
import time
import sys

from common import *

def main():

    start = time.time()

    os.chdir(src_folder)

    if not os.path.isfile(matplotlibrc):
        raise RuntimeError(f'Could not find: "{matplotlibrc}"')

    # gui
    cmd = cmd_common + ['-w', main_gui_py]
    gui_start_time = time.time()
    subprocess.call(cmd, shell=True)
    shutil_copy_verbose(matplotlibrc, os.path.join(dist_folder, os.path.splitext(main_gui_py)[0]))
    gui_time = time.time() - gui_start_time
    print(f"\nGUI build time: {int(gui_time//60)} min {int(gui_time%60)} sec")


if __name__ == "__main__":
    main()