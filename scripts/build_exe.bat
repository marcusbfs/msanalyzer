@echo off

REM Common variables
call "%~dp0variables.bat"

call %activate_venv%
call "%scripts_dir%\formatter.bat"
pyinstaller %main_py_file% -y -F --distpath "%dist_folder%" --workpath "%build_folder%"
pyinstaller %main_py_file% -y --distpath "%dist_folder%" --workpath "%build_folder%"
call %deactivate_venv%
