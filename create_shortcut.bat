rem @echo off

set sname=msanalyzer.bat

set p=%cd%
set exe=%p%\msanalyzer\msanalyzer.exe

(

    echo @echo off
    echo "%exe%" %%*

) > %sname%
