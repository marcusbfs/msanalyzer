python="C:\Users\Marcus\AppData\Local\Programs\Python\Python38\python.exe"
mpython="D:\Applications\msanalyzer\msanalyzer_venv\Scripts\python.exe"
uvicorn="D:\Applications\msanalyzer\msanalyzer_venv\Scripts\uvicorn.exe"

black:
	$(python) -m black csv_edem.py csv_edem_batch.py csv_edem_controller.py csv_edem_updater.py csv_input.py utils.py csv_edem_gui.py

f:
	$(mpython) api.py

server:
	$(uvicorn) api:app --reload --port 2342
