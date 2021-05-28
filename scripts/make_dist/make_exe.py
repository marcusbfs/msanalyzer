import time

import make_cli
import make_gui

start = time.time()

# cli
make_cli.main()

# gui
make_gui.main()

finish = time.time() - start
print(f"\nScript finished in {int(finish//60)} min {int(finish%60)} sec")
