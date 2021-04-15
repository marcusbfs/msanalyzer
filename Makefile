python=D:\Applications\msanalyzer\msanalyzer_venv\Scripts\python.exe


all:
	$(python) msanalyzer\msanalyzer_gui.py

black:
	$(python) -m black msanalyzer\msanalyzer_gui.py