import os
import subprocess
import time
import shutil

from PyInstaller.utils.hooks import exec_statement

def shutil_copy_verbose(src:str, dst:str) -> None:
    print(f'Copying "{src}" to "{dst}"')
    shutil.copy(src, dst)

def copytree2(source,dest):
    os.mkdir(dest)
    dest_dir = os.path.join(dest,os.path.basename(source))
    shutil.copytree(source,dest_dir)


start_time = time.time()

repo_dir = os.path.abspath('..')
python_exe = os.path.join(repo_dir, 'msanalyzer_venv', 'Scripts', 'python.exe')
main_py = os.path.join(repo_dir, 'msanalyzer','api.py')
matplotlibrc = os.path.join(repo_dir,'scripts', 'matplotlibrc')
dist_folder = os.path.join(repo_dir,'scripts', 'dist')
mpl_data_dir = os.path.join(repo_dir, 'msanalyzer_venv', 'Lib', 'site-packages', 'matplotlib', 'mpl-data')
mpl_destination = os.path.join(repo_dir, 'scripts', 'dist', 'api', 'matplotlib', 'mpl-data')

hidden_imports=[
                'uvicorn.logging',
                'uvicorn.loops',
                'uvicorn.loops.auto',
                'uvicorn.protocols',
                'uvicorn.protocols.http',
                'uvicorn.protocols.http.auto',
                'uvicorn.protocols.websockets',
                'uvicorn.protocols.websockets.auto',
                'uvicorn.lifespan',
                'uvicorn.lifespan.on',
            ]



hidden_matplotlib = ['matplotlib.backends.backend_svg', 'matplotlib.backends.backend_tkagg']
hidden_imports = hidden_imports + hidden_matplotlib

cmd_options = ['--clean', '--onedir', '--console']

for i in hidden_imports:
    cmd_options.append('--hidden-import')
    cmd_options.append(i)

cmd = [python_exe, '-m', 'PyInstaller'] + cmd_options + [main_py]

# subprocess.call(cmd, shell=True)
shutil_copy_verbose(matplotlibrc, os.path.join(dist_folder, os.path.splitext(os.path.basename(main_py))[0]))
shutil_copy_verbose(matplotlibrc, dist_folder)
shutil.copytree(mpl_data_dir,mpl_destination,dirs_exist_ok =True)

# copy to UI folder if...
ui_release_folder = os.path.join(repo_dir, 'UI','release')
if os.path.isdir(ui_release_folder):
    print("Copying to " + ui_release_folder)
    shutil.copytree(dist_folder,os.path.join(ui_release_folder, 'win-unpacked', 'resources','dist'),dirs_exist_ok =True)
    shutil_copy_verbose(matplotlibrc, os.path.join(ui_release_folder, 'win-unpacked', 'resources'))


elapsed_time = time.time() - start_time

if (elapsed_time > 60.0):
    print(f'\nElapsed time: {int(elapsed_time//60)}min{elapsed_time%60:.2f}seconds')
else:
    print(f'\nElapsed time: {elapsed_time:.2f} seconds')