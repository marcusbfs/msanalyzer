import os
import subprocess
import shutil
import time
import sys

from common import *

import make_cli
import make_gui

start = time.time()

cur_folder = os.path.abspath(".")
src_folder = os.path.join(os.path.abspath(".."), "msanalyzer")

# cli
make_cli.main()

# gui
make_gui.main()

finish = time.time() - start
print(f"\nScript finished in {int(finish//60)} min {int(finish%60)} sec")
