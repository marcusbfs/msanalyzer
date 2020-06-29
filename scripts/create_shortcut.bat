@echo off

REM Common variables

set p=%cd%
set exe=%p%\msanalyzer\msanalyzer.exe
set sname="msanalyzer.bat"

(
    echo @echo off
    echo "%exe%" %%*
) > %sname%
