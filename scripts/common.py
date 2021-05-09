import os

repo_dir = os.path.abspath("..")
python_exe = os.path.join(repo_dir, "msanalyzer_venv", "Scripts", "python.exe")
dist_folder = os.path.join(repo_dir, "scripts", "dist")
main_py = os.path.join(repo_dir,  "local_api.py")
# mpl data
matplotlibrc = os.path.join(repo_dir, "scripts", "matplotlibrc")
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
