import shutil
import sys
from pathlib import Path


def shutil_copy_verbose(src: Path, dst: Path) -> None:
    print(f'Copying "{src}" to "{dst}"')
    shutil.copy(src, dst)


cur_folder = Path(__file__).parent.absolute()
repo_folder = cur_folder.parent.parent.absolute()
src_folder = repo_folder / "src" / "msanalyzer"

python_exe = sys.executable
main_py: Path = cur_folder / "msanalyzer_cli.py"

main_gui_py: Path = Path("msanalyzer_gui.py")
hidden_imports = ["msanalyzer"]

matplotlibrc: Path = src_folder / "matplotlibrc"
dist_folder: Path = cur_folder / "dist"
build_folder: Path = cur_folder / "build"

cmd_common: list[str] = [
    python_exe,
    "-O",
    "-m",
    "PyInstaller",
    "--clean",
    "-D",
    "-y",
    "--distpath",
    str(dist_folder),
    "--workpath",
    str(build_folder),
    "--icon",
    "NONE",
]

for hm in hidden_imports:
    cmd_common.append("--hidden-import")
    cmd_common.append(hm)
