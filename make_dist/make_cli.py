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

    # cli
    cmd = cmd_common + ['-c', main_py]
    cli_start_time = time.time()
    subprocess.call(cmd, shell=True)
    shutil_copy_verbose(matplotlibrc, os.path.join(dist_folder, os.path.splitext(main_py)[0]))
    cli_time = time.time() - cli_start_time
    print(f"CLI build time: {int(cli_time//60)} min {int(cli_time%60)} sec")


if __name__ == "__main__":
    main()