import os
import subprocess
import time
import shutil

from make_server_dist import buildPyInstaller
from common import *

start_time = time.time()

cur_dir = os.getcwd()
# Build pyinstaller
buildPyInstaller()

# change dir an build UI
os.chdir(ui_folder)
subprocess.call(["yarn", "package"], shell=True)

# return to script folder and build dir
os.chdir(cur_dir)

elapsed_time = time.time() - start_time

print(f"\nFinished all in: {elapsed_time:.3f} seconds")
