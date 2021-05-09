python=D:\Applications\msanalyzer\msanalyzer_venv\Scripts\python.exe


dev:
	uvicorn msanalyzer.api:app --reload --port 2342

local:
	uvicorn msanalyzer.local_api:app --reload --port 2342

all:
	$(python) msanalyzer\msanalyzer_gui.py

black:
	$(python) -m black msanalyzer\msanalyzer_gui.py
