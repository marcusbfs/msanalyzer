import os
from pathlib import Path

scripts_dir = Path(__file__).parent.absolute()
repo_dir = scripts_dir.parent.absolute()
python_exe = os.path.join(repo_dir, "msanalyzer_venv", "Scripts", "python.exe")
dist_folder = scripts_dir / "dist"
main_py = os.path.join(repo_dir, "local_api.py")
# mpl data
matplotlibrc = scripts_dir / "matplotlibrc"
mpl_data_dir = os.path.join(
    repo_dir, "msanalyzer_venv", "Lib", "site-packages", "matplotlib", "mpl-data"
)
mpl_destination = os.path.join(
    repo_dir, "scripts", "dist", "local_api", "matplotlib", "mpl-data"
)
# UI
ui_folder = os.path.join(repo_dir, "UI")
ui_release_folder = os.path.join(ui_folder, "release")
ui_exe_folder = os.path.join(ui_release_folder, "win-unpacked")
