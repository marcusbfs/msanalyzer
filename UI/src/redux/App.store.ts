import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AppStateType {
  xpsfiles: Array<string>;
  outName: string;
  outDirName: string;
}

const initialState = {
  xpsfiles: [],
  outName: '',
  outDirName: '',
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
  },
});

export const { setXPSFiles, setOutName, setOutDir } = appSlice.actions;
export default appSlice.reducer;
