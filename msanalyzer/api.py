import io
import os
import json
import pathlib
import logging
import time
import shutil
import zipfile

from typing import Optional, List, Tuple, TypedDict

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse

from pydantic import BaseModel
import aiofiles
import uvicorn

import matplotlib.pyplot as plt

from . import MasterSizerReport as msreport
from . import MultipleFilesReport as multireport


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


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


@app.post("/getInputExample")
def getInputExample() -> FileResponse:
    input_example_file = os.path.join(parent_folder, "input_examples", "ms_input.xps")
    filename = "msanalyzer_input_example.xps"
    return FileResponse(
        path=input_example_file, filename=filename, media_type="application/oxps"
    )


class DictAlive(TypedDict):
    status: str
    author: str
    email: str


@app.get("/")
async def alive() -> DictAlive:
    return {
        "status": "running",
        "author": "Marcus Bruno Fernandes Silva",
        "email": "marcusbfs@gmail.com",
    }


@app.post("/singleModeZip")
async def singleModeZip(
    file: UploadFile = File(...),
    meanType: str = Form("geo"),
    zerosLeft: int = Form(1),
    zerosRight: int = Form(1),
    logScale: bool = Form(True),
    multiLabel: bool = Form(True),
) -> StreamingResponse:
    logger.debug(
        f"singleModeZip called with args: {meanType=}, {zerosLeft=}, {zerosRight=}, {logScale=}, {multiLabel=}"
    )

    timestr = time.strftime("%Y%m%d-%H%M%S") + "-" + str(time.time()).replace(".", "")
    basename_xps = os.path.splitext(file.filename)[0]
    base_xpsfile = basename_xps + "_" + timestr + "_.xps"
    xpsfile = os.path.join(current_folder, base_xpsfile)
    outputName = basename_xps
    outputDir = os.path.join(current_folder, "outDir_" + timestr)

    logger.info("Closing all figures")
    plt.clf()
    plt.close("all")

    if not os.path.isdir(outputDir):
        logger.info(f"Creating output dir: {outputDir}")
        os.mkdir(outputDir)

    reporter: msreport.MasterSizerReport = msreport.MasterSizerReport()

    reporter.setXPSfile(file.file._file, file.filename)
    reporter.setDiameterMeanType(
        msreport.DiameterMeanType.geometric
        if meanType == "geo"
        else msreport.DiameterMeanType.arithmetic
    )
    reporter.cutFirstZeroPoints(zerosLeft, tol=1e-8)
    reporter.cutLastZeroPoints(zerosRight, tol=1e-8)
    reporter.setLogScale(logscale=logScale)

    # calculate
    reporter.evaluateData()
    reporter.evaluateModels()

    # name of outputfiles
    curves = outputName + "_curves"
    curves_data = outputName + "_curves_data.txt"
    PSD_model = outputName + "_model"
    PSD_data = outputName + "_model_parameters"
    excel_data = outputName + "_curve_data"
    best_model_basename = outputName + "_best_models_ranking"

    fig = reporter.saveFig(outputDir, curves)
    models_figs = reporter.saveModelsFig(outputDir, PSD_model)
    reporter.saveData(outputDir, curves_data)
    reporter.saveModelsData(outputDir, PSD_data)
    reporter.saveExcel(outputDir, excel_data)

    reporter.saveBestModelsRanking(outputDir, best_model_basename)

    # zip folder
    logger.info("Creating zip in-memory")
    in_memory = io.BytesIO()
    zf = zipfile.ZipFile(in_memory, mode="w")

    for f in os.listdir(outputDir):
        ff = os.path.join(outputDir, f)
        # logger.debug(f"Appending to zip: {ff}")
        zf.write(ff, f, zipfile.ZIP_STORED)

    zf.close()
    in_memory.seek(0)

    # rm dir and file
    logger.info(f"Removing output dir: {outputDir}")
    shutil.rmtree(outputDir)

    response = StreamingResponse(
        in_memory,
        headers={
            "basename": basename_xps,
            "Content-Disposition": f"attachment;filename={basename_xps}.zip",
        },
        media_type="applicaton/zip",
    )
    return response


@app.post("/multiModeZip")
async def multiModeZip(
    files: List[UploadFile] = File(...),
    meanType: str = Form("geo"),
    zerosLeft: int = Form(1),
    zerosRight: int = Form(1),
    logScale: bool = Form(True),
    multiLabel: bool = Form(True),
) -> StreamingResponse:
    logger.debug(
        f"multiModeZip called with args: {meanType=}, {zerosLeft=}, {zerosRight=}, {logScale=}, {multiLabel=}"
    )
    number_of_files = len(files)

    timestr = time.strftime("%Y%m%d-%H%M%S") + "-" + str(time.time()).replace(".", "")
    basenames_xps = [os.path.splitext(f.filename)[0] for f in files]
    base_xpsfiles = [b + "_" + timestr + "_.xps" for b in basenames_xps]
    xpsfiles = [os.path.join(current_folder, b) for b in base_xpsfiles]
    outputName = "multiplos_arquivos"
    outputDir = os.path.join(current_folder, "outDir_" + timestr)

    logger.info("Closing all figures")
    plt.clf()
    plt.close("all")

    if not os.path.isdir(outputDir):
        logger.info(f"Creating output dir: {outputDir}")
        os.mkdir(outputDir)

    logger.warn(f"XPS files: {base_xpsfiles}")

    multiReporter = multireport.MultipleFilesReport(
        [f.file._file for f in files],
        basenames_xps,
        (
            msreport.DiameterMeanType.geometric
            if meanType == "geo"
            else msreport.DiameterMeanType.arithmetic
        ),
        logScale,
        zerosLeft,
        zerosRight,
        {},
        multiLabel,
    )

    if multiLabel:
        logger.info("Using multilabels")
        multiReporter.setLabels(basenames_xps)

    MultiSizeDistribution_output_file = os.path.join(
        outputDir, outputName + "_distribution"
    )
    MultiFrequency_output_file = os.path.join(outputDir, outputName + "_frequency")

    logger.info("Saving figures")
    multiReporter.frequencyPlot(MultiFrequency_output_file)
    multiReporter.sizeDistributionPlot(MultiSizeDistribution_output_file)

    # zip folder
    logger.info("Creating zip in-memory")
    in_memory = io.BytesIO()
    zf = zipfile.ZipFile(in_memory, mode="w")

    for f in os.listdir(outputDir):
        ff = os.path.join(outputDir, f)
        # logger.debug(f"Appending to zip: {ff}")
        zf.write(ff, f, zipfile.ZIP_STORED)

    zf.close()
    in_memory.seek(0)

    # rm dir and file
    logger.info(f"Removing output dir: {outputDir}")
    shutil.rmtree(outputDir)

    response = StreamingResponse(
        in_memory,
        headers={
            "basename": outputName,
            "Content-Disposition": f"attachment;filename={outputName}.zip",
        },
        media_type="applicaton/zip",
    )
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2342, reload=False)
