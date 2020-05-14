@echo off

REM Common variables
call "%~dp0variables.bat"

call "%scripts_dir%\formatter.bat"
call %activate_venv%
pyinstaller %main_py_file% -y -F --distpath "%dist_folder%" --workpath "%build_folder%" --hidden-import="pkg_resources.py2_warn"
pyinstaller %main_py_file% -y --distpath "%dist_folder%" --workpath "%build_folder%" --hidden-import="pkg_resources.py2_warn"
call %deactivate_venv%

set z7folder="C:\Program Files\7-Zip\"
set z7exe=%z7folder%"7z.exe"

copy %shortcut_creator% "%dist_folder%" /y
copy "%repo_dir%\ms_input.xps" "%dist_folder%" /y
copy "%repo_dir%\ms_input.xps" "%dist_folder%\ms_input_test.xps" /y

pushd "%dist_folder%"
call %z7exe% a -tzip "%dist_folder%/msanalyzer.zip" msanalyzer
call %z7exe% a -tzip "%dist_folder%/msanalyzer.zip" "%dist_folder%\ms_input_test.xps"
IF EXIST %shortcut_creator% (
    call %z7exe% a -tzip "%dist_folder%/msanalyzer.zip" %shortcut_creator%
)
popd