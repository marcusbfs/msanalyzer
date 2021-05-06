import os
import json
import pathlib
import logging
import time
import shutil

from typing import Optional, List, Tuple

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
CURRENT_SETTINGS = DEFAULT_OPTIONS

CURRENT_OPTIONS = DEFAULT_OPTIONS


def loadSettings(settings):
    options = {}
    if os.path.isfile(settings):
        with open(settings, "r") as f:
            options = json.loads(f.read())
    else:
        options = DEFAULT_OPTIONS
        with open(settings, "w") as f:
            json.dump(DEFAULT_OPTIONS, f)
    return options


def saveSettings(settings):
    try:
        with open(config_file, "w") as f:
            json.dump(settings, f)
        return settings
    except:
        # f = open(config_file)
        # json.dump(DEFAULT_OPTIONS, f)
        # f.close()
        with open(config_file, "w") as f:
            json.dump(DEFAULT_OPTIONS, f)
        return DEFAULT_OPTIONS


CURRENT_OPTIONS = loadSettings(config_file)


app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
# ]

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


list_of_diameterchoices = {
    "geo": msreport.DiameterMeanType.geometric,
    "ari": msreport.DiameterMeanType.arithmetic,
}


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


# @app.get('/getDir', response_model=Directory)
# async def getDir():
#     try:
#         root = Tk()
#         root.withdraw()
#         root.wm_attributes('-topmost', 1)

#         dirname = askdirectory()

#         if not dirname:
#             return {"dirname": "","rootdir" : "", "basename" :  ""}

#         dirname = os.path.abspath(dirname)
#         basename = os.path.splitext(dirname)[0]
#         rootdir = os.path.basename(dirname)
#         return {"dirname": dirname, "rootdir" : rootdir, "basename" :  basename}
#     except:
#         return {"dirname": "","rootdir" : "", "basename" :  ""}


# @app.get('/getConfig', response_model=CommonOptions)
# def getConfig():
#     return CURRENT_SETTINGS


@app.post("/getInputExample")
def getInputExample():
    input_example_file = os.path.join(parent_folder, "input_examples", "ms_input.xps")
    filename = "msanalyzer_input_example.xps"
    return FileResponse(
        path=input_example_file, filename=filename, media_type="application/oxps"
    )


# @app.post("/setConfig")
# def setConfig(options : CommonOptions):
#     global CURRENT_OPTIONS
#     CURRENT_OPTIONS = saveSettings(options.dict())


# @app.post('/getFiles', response_model=Files)
# async def getFiles(types : selectFileTypes):
#     try:
#         root = Tk()
#         root.withdraw()
#         root.wm_attributes('-topmost', 1)

#         if types.fileTypes:
#             files = askopenfilenames(filetypes=types.fileTypes)
#         else:
#             files = askopenfilenames()

#         basenames = [ os.path.splitext(os.path.basename(f))[0] for f in files]
#         files = [os.path.abspath(f) for f in files]
#         dirnames = [ os.path.dirname(f) for f in files]
#         return {"files": files, "basenames" : basenames, "dirnames" :  dirnames}
#     except:
#         return {"files": [], "basenames" : [], "dirnames" :  []}

# @app.get("/open/{path}")
# async def open(path : str):
#     if (os.path.isfile(path) or os.path.isdir(path)):
#         os.startfile(path)


@app.get("/")
async def alive():
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
):
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

    # save file
    async with aiofiles.open(xpsfile, "wb") as out_file:
        logger.info(f'Saving XPS file: "{xpsfile}"')
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    reporter: msreport.MasterSizerReport = msreport.MasterSizerReport()

    reporter.setXPSfile(xpsfile)
    reporter.setDiameterMeanType(list_of_diameterchoices[meanType])
    reporter.cutFirstZeroPoints(zerosLeft, tol=1e-8)
    reporter.cutLastZeroPoints(zerosRight, tol=1e-8)
    reporter.setLogScale(logscale=zerosRight)

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

    # clean all zip and xps
    os.remove(xpsfile)
    for f in os.listdir(current_folder):
        if f.endswith(".zip") or f.endswith(".xps"):
            filepath = os.path.join(current_folder, f)
            logger.info(f"Removing {filepath}")
            os.remove(filepath)

    # zip folder
    xps_zip = basename_xps + "_" + timestr
    full_xps_zip = os.path.join(current_folder, xps_zip + ".zip")
    shutil.make_archive(os.path.join(current_folder, xps_zip), "zip", outputDir)

    # rm dir and file
    shutil.rmtree(outputDir)

    response = FileResponse(
        path=full_xps_zip, filename=xps_zip + ".zip", headers={"basename": basename_xps}
    )
    return response

    # @app.post('/singleModeCompute')
    # async def singleModeCompute(xpsfile : str, outputName : str, outputDir : str, options : CommonOptions):
    #     reporter : msreport.MasterSizerReport = msreport.MasterSizerReport()

    #     meanType = list_of_diameterchoices[options.meanType]
    #     number_of_zero_first = options.zerosLeft
    #     number_of_zero_last = options.zerosRight
    #     log_scale = options.logScale

    #     reporter.setXPSfile(xpsfile)
    #     reporter.setDiameterMeanType(meanType)
    #     reporter.cutFirstZeroPoints(number_of_zero_first, tol=1e-8)
    #     reporter.cutLastZeroPoints(number_of_zero_last, tol=1e-8)
    #     reporter.setLogScale(logscale=log_scale)

    #     # calculate
    #     reporter.evaluateData()
    #     reporter.evaluateModels()

    #     # name of outputfiles
    #     curves = outputName + "_curves"
    #     curves_data = outputName + "_curves_data.txt"
    #     PSD_model = outputName + "_model"
    #     PSD_data = outputName + "_model_parameters"
    #     excel_data = outputName + "_curve_data"
    #     best_model_basename = outputName + "_best_models_ranking"

    #     fig = reporter.saveFig(outputDir, curves)
    #     models_figs = reporter.saveModelsFig(outputDir, PSD_model)
    #     reporter.saveData(outputDir, curves_data)
    #     reporter.saveModelsData(outputDir, PSD_data)
    #     reporter.saveExcel(outputDir, excel_data)

    #     reporter.saveBestModelsRanking(outputDir, best_model_basename)

    # @app.post('/multiModeCompute')
    # async def multiModeCompute(multiInput : MultiInput, options : CommonOptions):
    #     number_of_files = len(multiInput.xpsfiles)

    #     meanType = list_of_diameterchoices[options.meanType]

    #     multiReporter = multireport.MultipleFilesReport(
    #         multiInput.xpsfiles,
    #         meanType,
    #         options.logScale,
    #         options.zerosLeft,
    #         options.zerosRight,
    #         {},
    #         options.multiLabel
    #     )

    #     if options.multiLabel and len(multiInput.labels) > 1:
    #         multiReporter.setLabels(multiInput.labels)

    #     MultiSizeDistribution_output_file = os.path.join(
    #         multiInput.outDir, multiInput.outName + '_distribution'
    #     )
    #     MultiFrequency_output_file = os.path.join(multiInput.outDir,multiInput.outName + "_frequency")

    #     multiReporter.frequencyPlot(MultiFrequency_output_file)

    # @app.post("/uploadfile/")
    # async def create_upload_file(file: UploadFile = File(...)):
    #     content = await file.read()
    #     return {"filename": file.filename, "content" : content}

    pass


@app.post("/multiModeZip")
async def multiModeZip(
    files: List[UploadFile] = File(...),
    meanType: str = Form("geo"),
    zerosLeft: int = Form(1),
    zerosRight: int = Form(1),
    logScale: bool = Form(True),
    multiLabel: bool = Form(True),
):
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

    # Save all files
    logger.info(f"Saving all files ({number_of_files} in total)")
    for file, xpsfile in zip(files, xpsfiles):
        async with aiofiles.open(xpsfile, "wb") as out_file:
            logger.info(f'Saving XPS file: "{xpsfile}"')
            content = await file.read()  # async read
            await out_file.write(content)  # async write

    meanType = list_of_diameterchoices[meanType]

    multiReporter = multireport.MultipleFilesReport(
        xpsfiles, meanType, logScale, zerosLeft, zerosRight, {}, multiLabel
    )

    if multiLabel:
        logger.info("Using multilabels")
        multiReporter.setLabels(basenames_xps)

    MultiSizeDistribution_output_file = os.path.join(
        outputDir, outputName + "_distribution"
    )
    MultiFrequency_output_file = os.path.join(outputDir, outputName + "_frequency")

    logger.info('Saving figures')
    multiReporter.frequencyPlot(MultiFrequency_output_file)
    multiReporter.sizeDistributionPlot(MultiSizeDistribution_output_file)

    # clean all zip and xps
    for xpsfile in xpsfiles:
        logger.info(f'Removing "{xpsfile}"')
        os.remove(xpsfile)

    for f in os.listdir(current_folder):
        if f.endswith(".zip") or f.endswith(".xps"):
            filepath = os.path.join(current_folder, f)
            logger.info(f"Removing {filepath}")
            os.remove(filepath)

    # zip folder
    xps_zip = outputName + "_" + timestr
    full_xps_zip = os.path.join(current_folder, xps_zip + ".zip")
    shutil.make_archive(os.path.join(current_folder, xps_zip), "zip", outputDir)

    # rm dir and file
    shutil.rmtree(outputDir)

    response = FileResponse(
        path=full_xps_zip, filename=xps_zip + ".zip", headers={"basename": outputName}
    )
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2342, reload=False)
    example_path = os.path.join(parent_folder, "input_examples", "ms_input.xps")
    print(example_path)
