from fastapi import FastAPI
from pydantic import BaseModel
import pathlib
import uvicorn
from tkinter import Tk  
from typing import Optional, List, Tuple
from tkinter.filedialog import askdirectory, askopenfilenames 
import json
import os

app = FastAPI()

current_folder = pathlib.Path(__file__).parent.absolute()

class selectFileTypes(BaseModel):
    fileTypes : Optional[List[Tuple[str, str]]] = None

class Files(BaseModel):
    files : List[str]
    dirnames : List[str]
    basenames : List[str]


class Directory(BaseModel):
    dirname : str
    rootdir : str
    basename : str

@app.get('/getDir', response_model=Directory)
async def getDir():
    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)

        dirname = os.path.abspath(askdirectory())
        basename = os.path.splitext(dirname)[0]
        rootdir = os.path.basename(dirname)
        return {"dirname": dirname, "rootdir" : rootdir, "basename" :  basename}
    except:
        return {"dirname": "","rootdir" : "", "basename" :  ""}




@app.post('/getFiles', response_model=Files)
async def getFiles(types : selectFileTypes):
    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)

        if types.fileTypes:
            files = askopenfilenames(filetypes=types.fileTypes)
        else:
            files = askopenfilenames()

        basenames = [ os.path.splitext(os.path.basename(f))[0] for f in files]
        files = [os.path.abspath(f) for f in files]
        dirnames = [ os.path.dirname(f) for f in files]
        return {"files": files, "basenames" : basenames, "dirnames" :  dirnames}
    except:
        return {"files": [], "basenames" : [], "dirnames" :  []}

@app.get("/open/{path}")
async def open(path : str):
    if (os.path.isfile(path) or os.path.isdir(path)):
        os.startfile(path)

@app.get("/")
async def alive():
    return {"status": "running"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=2342, reload=False)