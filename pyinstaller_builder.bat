call msanalyzer_venv\Scripts\activate.bat
call black_formatter.bat

set z7folder="C:\Program Files\7-Zip\"
set z7exe=%z7folder%"7z.exe"
set shortcut_creator=create_shortcut.bat

pyinstaller msanalyzer.py -y

copy create_shortcut.bat dist /y
copy ms_input.xps dist /y
copy ms_input.xps dist\ms_input_test.xps /y

cd dist
call %z7exe% a -tzip ../msanalyzer.zip msanalyzer
IF EXIST %shortcut_creator% (
    call %z7exe% a -tzip ../msanalyzer.zip %shortcut_creator%
)
cd ..
