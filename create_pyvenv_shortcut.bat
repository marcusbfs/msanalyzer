rem @echo off

set sname=msanalyzer.bat

set p=%cd%
set exe=%p%\msanalyzer_venv\Scripts\python.exe
set main_py=%p%\msanalyzer.py

(

    echo @echo off
    echo "%exe%" "%main_py%" %%*

) > %sname%
