rem @echo off

REM Common variables
call "%~dp0variables.bat"

(
    echo @echo off
    echo %python_exe% %main_py_file% %%*

) > %sname%
