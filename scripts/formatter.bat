@echo off

REM Common variables
call "%~dp0variables.bat"

call %activate_venv%
pushd "%src_dir%"
for /r %%i in (*.py) do black %%i
popd
call %deactivate_venv%