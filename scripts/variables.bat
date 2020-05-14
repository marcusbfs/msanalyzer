@echo off
REM config
set main_name=msanalyzer
REM auto
set scripts_dir=%~dp0
set repo_dir=%scripts_dir%..
set src_dir=%repo_dir%\%main_name%
set shortcut_creator="%repo_dir%\scripts\create_shortcut.bat"
set venv_name=%main_name%_venv
set venv_dir=%repo_dir%\%venv_name%
set activate_venv="%venv_dir%\Scripts\activate.bat"
set deactivate_venv="%venv_dir%\Scripts\deactivate.bat"
set main_py_file="%src_dir%\%main_name%.py"
set build_folder=%repo_dir%\build
set dist_folder=%repo_dir%\dist
set python_exe="%venv_dir%\Scripts\python.exe"
set sname=%main_name%.bat