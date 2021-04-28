import os
import json
import pathlib
from tkinter import Tk  
from typing import Optional, List, Tuple
from tkinter.filedialog import askdirectory, askopenfilenames 

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

import MasterSizerReport as msreport
import MultipleFilesReport as multireport

app = FastAPI()

current_folder = pathlib.Path(__file__).parent.absolute()

list_of_diameterchoices = {
"geo": msreport.DiameterMeanType.geometric,
"ari": msreport.DiameterMeanType.arithmetic,
}

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

class CommonOptions(BaseModel):
    meanType : str 
    zerosLeft : int
    zerosRight : int
    logScale : bool
    multiLabel : bool

class MultiInput(BaseModel):
    xpsfiles : List[str]
    labels : List[str]
    outDir : str
    outName : str

@app.get('/getDir', response_model=Directory)
async def getDir():
    try:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)

        dirname = askdirectory()

        if not dirname:
            return {"dirname": "","rootdir" : "", "basename" :  ""}

        dirname = os.path.abspath(dirname)
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


@app.post('/singleModeCompute')
async def singleModeCompute(xpsfile : str, outputName : str, outputDir : str, options : CommonOptions):
    reporter : msreport.MasterSizerReport = msreport.MasterSizerReport()

    meanType = list_of_diameterchoices[options.meanType]
    number_of_zero_first = options.zerosLeft
    number_of_zero_last = options.zerosRight
    log_scale = options.logScale

    reporter.setXPSfile(xpsfile)
    reporter.setDiameterMeanType(meanType)
    reporter.cutFirstZeroPoints(number_of_zero_first, tol=1e-8)
    reporter.cutLastZeroPoints(number_of_zero_last, tol=1e-8)
    reporter.setLogScale(logscale=log_scale)

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


@app.post('/multiModeCompute')
async def multiModeCompute(multiInput : MultiInput, options : CommonOptions):
    number_of_files = len(multiInput.xpsfiles)

    meanType = list_of_diameterchoices[options.meanType]

    multiReporter = multireport.MultipleFilesReport(
        multiInput.xpsfiles,
        meanType,
        options.logScale,
        options.zerosLeft,
        options.zerosRight,
        {},
        options.multiLabel
    )

    if options.multiLabel and len(multiInput.labels) > 1:
        multiReporter.setLabels(multiInput.labels)

    MultiSizeDistribution_output_file = os.path.join(
        multiInput.outDir, multiInput.outName + '_distribution'
    )
    MultiFrequency_output_file = os.path.join(multiInput.outDir,multiInput.outName + "_frequency")

    multiReporter.frequencyPlot(MultiFrequency_output_file)


    pass
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=2342, reload=False)
