import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export enum MeanType {
  geo = 1,
  ari = 2,
}

interface AppStateType {
  xpsfiles: Array<string>;
  basenames: Array<string>;
  dirnames: Array<string>;
  outName: string;
  singleSVGfile: string;
  outDirName: string;
  isLogScale: boolean;
  meanType: MeanType;
  multiLabel: boolean;
  zerosLeft: number;
  zerosRight: number;
  isComputing: boolean;
  isSpinnerHidden: boolean;
  isServerOn: boolean;
  isSingleFile: boolean;
}

const initialState = {
  xpsfiles: [],
  basenames: [],
  dirnames: [],
  outName: '',
  outDirName: '',
  singleSVGfile: '',
  isLogScale: true,
  multiLabel: true,
  meanType: MeanType.geo,
  zerosLeft: 1,
  zerosRight: 1,
  isSpinnerHidden: true,
  isComputing: false,
  isServerOn: true,
  isSingleFile: true,
} as AppStateType;

const appSlice = createSlice({
  name: 'app',
  initialState,
  reducers: {
    setXPSFiles(state: AppStateType, action: PayloadAction<Array<string>>) {
      state.xpsfiles = action.payload;
    },
    setBasenames(state: AppStateType, action: PayloadAction<Array<string>>) {
      state.basenames = action.payload;
    },
    setDirnames(state: AppStateType, action: PayloadAction<Array<string>>) {
      state.dirnames = action.payload;
    },
    setOutName(state: AppStateType, action: PayloadAction<string>) {
      state.outName = action.payload;
    },
    setSingleSVGfile(state: AppStateType, action: PayloadAction<string>) {
      state.singleSVGfile = action.payload;
    },
    setOutDir(state: AppStateType, action: PayloadAction<string>) {
      state.outDirName = action.payload;
    },
    toggleIsLogScale(state: AppStateType) {
      state.isLogScale = !state.isLogScale;
    },
    toggleMultiLabel(state: AppStateType) {
      state.multiLabel = !state.multiLabel;
    },
    setMeanType(state: AppStateType, action: PayloadAction<MeanType>) {
      state.meanType = action.payload;
    },
    setZerosLeft(state: AppStateType, action: PayloadAction<number>) {
      state.zerosLeft = action.payload;
    },
    setZerosRight(state: AppStateType, action: PayloadAction<number>) {
      state.zerosRight = action.payload;
    },
    setIsSpinnerHidden(state: AppStateType, action: PayloadAction<boolean>) {
      state.isSpinnerHidden = action.payload;
    },
    setIsComputing(state: AppStateType, action: PayloadAction<boolean>) {
      state.isComputing = action.payload;
    },
    setIsServerOn(state: AppStateType, action: PayloadAction<boolean>) {
      state.isServerOn = action.payload;
    },
    setIsSingleFile(state: AppStateType, action: PayloadAction<boolean>) {
      state.isSingleFile = action.payload;
    },
  },
});

export const {
  setXPSFiles,
  setBasenames,
  setDirnames,
  setOutName,
  setOutDir,
  toggleIsLogScale,
  toggleMultiLabel,
  setZerosLeft,
  setZerosRight,
  setMeanType,
  setIsSpinnerHidden,
  setIsComputing,
  setIsServerOn,
  setIsSingleFile,
  setSingleSVGfile,
} = appSlice.actions;
export default appSlice.reducer;
