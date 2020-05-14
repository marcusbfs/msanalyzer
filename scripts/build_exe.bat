REM Common variables
call "%~dp0variables.bat"

call %activate_venv%

black %main_py_file%
pyinstaller %main_py_file% -y -F --distdir "%dist_folder%" --workdir "%build_folder%"