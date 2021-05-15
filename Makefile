python=D:\Applications\msanalyzer\msanalyzer_venv\Scripts\python.exe


.PHONY = fmt

fmt:
	autoflake -i --remove-unused-variables --remove-all-unused-imports msanalyzer-cli.py 
	isort msanalyzer-cli.py msanalyzer make_dist scripts
	black msanalyzer-cli.py msanalyzer make_dist scripts

dev:
	uvicorn msanalyzer.api:app --reload --port 2342

local:
	uvicorn local_api:app --reload --port 2342

all:
	$(python) msanalyzer\msanalyzer_gui.py

black:
	$(python) -m black msanalyzer\msanalyzer_gui.py
