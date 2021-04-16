import os
import subprocess
import shutil
import time
import sys

def shutil_copy_verbose(src:str, dst:str) -> None:
    print(f'Copying "{src}" to "{dst}"')
    shutil.copy(src, dst)

start = time.time()

python_exe = sys.executable
main_py = 'msanalyzer.py'
main_gui_py = 'msanalyzer_gui.py'
hidden_matplotlib = ['matplotlib.backends.backend_svg', 'matplotlib.backends.backend_tkagg']
matplotlibrc = 'matplotlibrc'
dist_folder = '.\dist'
build_folder = r'.\build'

if not os.path.isfile(matplotlibrc):
    raise RuntimeError(f'Could not find: "{matplotlibrc}"')

cmd_common = [python_exe, '-m', 'PyInstaller', '--clean', '-D', '-y','--distpath', dist_folder, '--workpath', build_folder]

for hm in hidden_matplotlib:
    cmd_common.append('--hidden-import')
    cmd_common.append(hm)

# cli
cmd = cmd_common + ['-c', main_py]
cli_start_time = time.time()
subprocess.call(cmd, shell=True)
shutil_copy_verbose(matplotlibrc, os.path.join(dist_folder, os.path.splitext(main_py)[0]))
cli_time = time.time() - cli_start_time
print(f"CLI build time: {int(cli_time//60)} min {int(cli_time%60)} sec")

# gui
cmd = cmd_common + ['-w', main_gui_py]
gui_start_time = time.time()
subprocess.call(cmd, shell=True)
shutil_copy_verbose(matplotlibrc, os.path.join(dist_folder, os.path.splitext(main_gui_py)[0]))
gui_time = time.time() - gui_start_time
print(f"GUI build time: {int(gui_time//60)} min {int(gui_time%60)} sec")

finish = time.time() - start
print(f"\nScript finished in {int(finish//60)} min {int(finish%60)} sec")