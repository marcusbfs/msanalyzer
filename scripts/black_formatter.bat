@echo off
SET mypath=%~dp0
set py_folder=%mypath%..

call "%py_folder%\msanalyzer_venv\Scripts\activate.bat"

black "%py_folder%\msanalyzer.py"
black "%py_folder%\MasterSizerInput.py"
black "%py_folder%\MasterSizerReport.py"

call "%py_folder%\msanalyzer_venv\Scripts\deactivate.bat"
