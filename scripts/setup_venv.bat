@echo off

REM Common variables
call "%~dp0variables.bat"

python -m venv "%venv_dir%"
call %activate_venv%
pip install -r "%repo_dir%\requirements.txt"
call %deactivate_venv%