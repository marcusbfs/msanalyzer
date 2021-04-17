import os
import subprocess
import shutil
import time
import sys

def shutil_copy_verbose(src:str, dst:str) -> None:
    print(f'Copying "{src}" to "{dst}"')
    shutil.copy(src, dst)

cur_folder = os.path.abspath('.')
src_folder = os.path.join(os.path.abspath('..'), 'msanalyzer')

python_exe = sys.executable
main_py = 'msanalyzer.py'
main_gui_py = 'msanalyzer_gui.py'
hidden_matplotlib = ['matplotlib.backends.backend_svg', 'matplotlib.backends.backend_tkagg']
matplotlibrc = os.path.join(src_folder, 'matplotlibrc')
dist_folder = os.path.join(cur_folder, 'dist')
build_folder = os.path.join(cur_folder, 'build')

cmd_common = [python_exe, '-m', 'PyInstaller', '--clean', '-D', '-y','--distpath', dist_folder, '--workpath', build_folder]

for hm in hidden_matplotlib:
    cmd_common.append('--hidden-import')
    cmd_common.append(hm)