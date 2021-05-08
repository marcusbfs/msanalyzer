import os

repo_dir = os.path.abspath("..")
src_dir = os.path.join(repo_dir, "msanalyzer")

env_name = "msanalyzer_venv"
python_exe = os.path.join(repo_dir, env_name, "Scripts", "python.exe")
pythonw_exe = os.path.join(repo_dir, env_name, "Scripts", "pythonw.exe")

if (not os.path.isfile(python_exe)) or (not os.path.isfile(pythonw_exe)):
    raise RuntimeError(f"Please, set up the virtual env first!")

main_py = os.path.join(repo_dir, "msanalyzer-cli.py")
main_gui_py = os.path.join(src_dir, "msanalyzer_gui.py")

if not os.path.isfile(main_py):
    raise RuntimeError(f'Could not find "{main_py}"')

if not os.path.isfile(main_gui_py):
    raise RuntimeError(f'Could not find "{main_gui_py}"')

main_bat = "msanalyzer.bat"
main_gui_bat = "msanalyzer_gui.bat"

with open(main_bat, "w") as main:
    main.write("@echo off\n")
    main.write(f'"{python_exe}" "{main_py}" %*\n')

with open(main_gui_bat, "w") as main_gui:
    main_gui.write("@echo off\n")
    main_gui.write(f'start "" "{pythonw_exe}" "{main_gui_py}"\n')
