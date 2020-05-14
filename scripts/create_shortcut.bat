@echo off

REM Common variables
call "%~dp0variables.bat"

set p=%cd%
set exe=%p%\msanalyzer\msanalyzer.exe

(
    echo @echo off
    echo "%exe%" %%*
) > %sname%
