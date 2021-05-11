import logging
import os
import pathlib
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilenames
from typing import List, Optional, Tuple

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from msanalyzer import MasterSizerReport as msreport
from msanalyzer import local_api_helper as LAH

logging.getLogger("matplotlib.font_manager").disabled = True

app = FastAPI()

current_folder = pathlib.Path(__file__).parent.absolute()

list_of_diameterchoices = {
    "geo": msreport.DiameterMeanType.geometric,
    "ari": msreport.DiameterMeanType.arithmetic,
}


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
logger.addHandler(c_handler)

logging.getLogger("matplotlib.font_manager").disabled = True

current_folder = pathlib.Path(__file__).parent.absolute()
parent_folder = os.path.dirname(current_folder)

config_file = os.path.join(current_folder, "msanalyzer_config.json")

DEFAULT_OPTIONS = {
    "meanType": "geo",
    "zerosLeft": 1,
    "zerosRight": 1,
    "logScale": True,
    "multiLabel": True,
}

app = FastAPI()

origins = [
    "*",
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["*"],
# )


class selectFileTypes(BaseModel):
    fileTypes: Optional[List[Tuple[str, str]]] = None


class Files(BaseModel):
    files: List[str]
    dirnames: List[str]
    basenames: List[str]


class Directory(BaseModel):
    dirname: str
    rootdir: str
    basename: str


class CommonOptions(BaseModel):
    meanType: str
    zerosLeft: int
    zerosRight: int
    logScale: bool
    multiLabel: bool


class MultiInput(BaseModel):
    xpsfiles: List[str]
    labels: List[str]
    outDir: str
    outName: str


# ==== local api ====================================================================


@app.get("/getDir", response_model=Directory)
async def getDir():
    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)

        dirname = askdirectory()

        if not dirname:
            return {"dirname": "", "rootdir": "", "basename": ""}

        dirname = os.path.abspath(dirname)
        basename = os.path.splitext(dirname)[0]
        rootdir = os.path.basename(dirname)
        return {"dirname": dirname, "rootdir": rootdir, "basename": basename}
    except:
        return {"dirname": "", "rootdir": "", "basename": ""}


@app.post("/getFiles", response_model=Files)
async def getFiles(types: selectFileTypes):
    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)

        if types.fileTypes:
            files = askopenfilenames(filetypes=types.fileTypes)
        else:
            files = askopenfilenames()

        basenames = [os.path.splitext(os.path.basename(f))[0] for f in files]
        files = [os.path.abspath(f) for f in files]
        dirnames = [os.path.dirname(f) for f in files]
        return {"files": files, "basenames": basenames, "dirnames": dirnames}
    except:
        return {"files": [], "basenames": [], "dirnames": []}


@app.get("/open/{path}")
async def open(path: str):
    if os.path.isfile(path) or os.path.isdir(path):
        os.startfile(path)


@app.get("/")
async def alive():
    return {"status": "running"}


@app.post("/singleModeCompute")
async def singleModeCompute(
    xpsfile: str, outputName: str, outputDir: str, options: CommonOptions
):
    await LAH.singleModeCompute_helper(xpsfile, outputName, outputDir, options)


@app.post("/multiModeCompute")
async def multiModeCompute(multiInput: MultiInput, options: CommonOptions):
    await LAH.multiModeCompute_helper(multiInput, options)


# ==== end of local api =============================================================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2342, reload=False)
