@echo off
SET mypath=%~dp0
set py_folder=%mypath%..
set build="%py_folder%\build"
set dist="%py_folder%\dist"
set zipfile="%dist%\msanalyzer.zip"
set z7folder="C:\Program Files\7-Zip\"
set z7exe=%z7folder%"7z.exe"
set shortcut_creator="%py_folder%\scripts\create_shortcut.bat"

pushd "%mypath%"

call "%py_folder%\scripts\black_formatter.bat"

rem execute pyinstaller
call "%py_folder%\msanalyzer_venv\Scripts\activate.bat"

call :pyinstaller_folder
call :pyinstaller_exe

call "%py_folder%\msanalyzer_venv\Scripts\deactivate.bat"

copy %shortcut_creator% "%dist%" /y
copy "%py_folder%\ms_input.xps" "%dist%" /y
copy "%py_folder%\ms_input.xps" "%dist%\ms_input_test.xps" /y

call :zip_folder
call "%py_folder%\scripts\clean_build.bat"

popd

rem exit main function
exit /b 0

REM ============================ functions ======================================
:pyinstaller_folder
pyinstaller "%py_folder%\msanalyzer.py" -y --distpath "%dist%" --workpath "%build%"
exit /b 0

:pyinstaller_exe
pyinstaller "%py_folder%\msanalyzer.py" -y -F --distpath "%dist%" --workpath "%build%"
exit /b 0

:zip_folder
cd "%dist%"
call %z7exe% a -tzip %zipfile% msanalyzer
IF EXIST %shortcut_creator% (
    call %z7exe% a -tzip %zipfile% %shortcut_creator%
)
cd ..
exit /b 0