import os
import subprocess
import time


start_time = time.time()

repo_dir = os.path.abspath('..')
python_exe = os.path.join(repo_dir, 'env', 'Scripts', 'python.exe')
main_py = 'csv_edem_api.py'

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

cmd_options = ['--clean', '--onedir', '--console']

for i in hidden_imports:
    cmd_options.append('--hidden-import')
    cmd_options.append(i)

cmd = [python_exe, '-m', 'PyInstaller'] + cmd_options + [main_py]

subprocess.call(cmd, shell=True)

elapsed_time = time.time() - start_time

if (elapsed_time > 60.0):
    print(f'\nElapsed time: {int(elapsed_time//60)}min{elapsed_time%60:.2f}seconds')
else:
    print(f'\nElapsed time: {elapsed_time:.2f} seconds')