import shutil
import sys
from pathlib import Path


def shutil_copy_verbose(src: Path, dst: Path) -> None:
    print(f'Copying "{src}" to "{dst}"')
    shutil.copy(src, dst)


cur_folder = Path(__file__).parent.absolute()
repo_folder = cur_folder.parent.absolute()
src_folder = repo_folder / "msanalyzer"

python_exe = sys.executable
main_py: Path = repo_folder / "msanalyzer-cli.py"

main_gui_py: Path = "msanalyzer_gui.py"
hidden_matplotlib = [
    "matplotlib.backends.backend_svg",
    "matplotlib.backends.backend_tkagg",
]
matplotlibrc: Path = src_folder / "matplotlibrc"
dist_folder: Path = cur_folder / "dist"
build_folder: Path = cur_folder / "build"

cmd_common: list[str] = [
    python_exe,
    "-m",
    "PyInstaller",
    "--clean",
    "-D",
    "-y",
    "--distpath",
    str(dist_folder),
    "--workpath",
    str(build_folder),
]

for hm in hidden_matplotlib:
    cmd_common.append("--hidden-import")
    cmd_common.append(hm)
