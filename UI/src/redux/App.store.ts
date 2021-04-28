import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export enum MeanType {
  geo = 1,
  ari = 2,
}

interface AppStateType {
  xpsfiles: Array<string>;
  outName: string;
  outDirName: string;
  isLogScale: boolean;
  meanType: MeanType;
  multiLabel: boolean;
  zerosLeft: number;
  zerosRight: number;
}

const initialState = {
  xpsfiles: [],
  outName: '',
  outDirName: '',
  isLogScale: true,
  multiLabel: true,
  meanType: MeanType.geo,
  zerosLeft: 1,
  zerosRight: 1,
} as AppStateType;

const appSlice = createSlice({
  name: 'app',
  initialState,
  reducers: {
    setXPSFiles(state: AppStateType, action: PayloadAction<Array<string>>) {
      state.xpsfiles = action.payload;
    },
    setOutName(state: AppStateType, action: PayloadAction<string>) {
      state.outName = action.payload;
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
  },
});

export const {
  setXPSFiles,
  setOutName,
  setOutDir,
  toggleIsLogScale,
  toggleMultiLabel,
  setZerosLeft,
  setZerosRight,
  setMeanType,
} = appSlice.actions;
export default appSlice.reducer;
