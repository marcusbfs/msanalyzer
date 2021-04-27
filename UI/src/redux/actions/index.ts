export const setXPS = (files: Array<string>) => {
  return {
    type: 'setXPS',
    payload: files,
  };
};

export const setOutDir = (outdir: string) => {
  return {
    type: 'setOutDir',
    payload: outdir,
  };
};

export const setOutName = (outname: string) => {
  return {
    type: 'setOutName',
    payload: outname,
  };
};
