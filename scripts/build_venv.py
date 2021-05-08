import os
import sys
import subprocess
import pathlib
import time

start_time = time.time()

scripts_dir = pathlib.Path(__file__).parent.absolute()
repo_dir = os.path.abspath(os.path.join(scripts_dir, ".."))
src_dir = os.path.join(repo_dir, "msanalyzer")
req_file = os.path.join(repo_dir, "requirements.txt")
dev_req_file = os.path.join(repo_dir, "dev-requirements.txt")

env_name = "msanalyzer_venv"
python_exe = sys.executable
env_python_exe = os.path.join(repo_dir, env_name, "Scripts", "python.exe")

print(f"Using python: {python_exe}")

os.chdir(repo_dir)
print(f"Current dir: {os.path.abspath(os.path.curdir)}")

print(f"Creating venv {env_name}")
subprocess.call([python_exe, "-m", "venv", env_name])

print("Upgrading pip...")
subprocess.call([env_python_exe, "-m", "pip", "install", "--upgrade", "pip"])

print("Installing requirements")
subprocess.call([env_python_exe, "-m", "pip", "install", "-r", req_file])

ans = input("Install dev requirements? ")

if ans.lower() in ("y", "yes", "s", "sim"):
    print("Installing dev requirements")
    subprocess.call([env_python_exe, "-m", "pip", "install", "-r", dev_req_file])

time_passed = time.time() - start_time
print(f"\nFinished in {time_passed:.2f} seconds")
