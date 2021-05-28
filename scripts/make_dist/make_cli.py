import os
import subprocess
import time

import common as C


def main() -> None:

    time.time()

    os.chdir(C.src_folder)

    if not C.matplotlibrc.is_file():
        raise RuntimeError(f'Could not find: "{C.matplotlibrc}"')

    # cli
    cmd = C.cmd_common + ["-c", str(C.main_py), "--name", "msanalyzercli"]

    print("Command:")
    print(cmd)

    cli_start_time = time.time()
    subprocess.call(cmd, shell=True)
    C.shutil_copy_verbose(
        C.matplotlibrc, C.dist_folder / C.main_py.name.replace(C.main_py.suffix, "")
    )
    cli_time = time.time() - cli_start_time
    print(f"\nCLI build time: {int(cli_time//60)} min {int(cli_time%60)} sec")


if __name__ == "__main__":
    main()
