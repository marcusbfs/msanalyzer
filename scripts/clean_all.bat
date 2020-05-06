SET p=%~dp0

call "%p%clean_build.bat"

pushd "%p%.."
del /f /s /q msanalyzer.zip 1>nul
popd
