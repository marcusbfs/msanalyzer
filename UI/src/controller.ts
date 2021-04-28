const base_url = 'http://127.0.0.1:2342/';

export interface CommonOptions {
  meanType: string;
  zerosLeft: number;
  zerosRight: number;
  logScale: boolean;
  multiLabel: boolean;
}

export function getXPSFiles(): Promise<{
  files: Array<string>;
  basenames: Array<string>;
  dirnames: Array<string>;
}> {
  const options = {
    fileTypes: [['Arquivos XPS', '.xps']],
  };

  return fetch(base_url + 'getFiles', {
    method: 'post',
    body: JSON.stringify(options),
  })
    .then((r) => {
      return r.json();
    })
    .catch((e) => {
      console.log('Error: ' + e);
      return null;
    });
}

export async function singleModeCompute(
  xpsfile: string,
  outputName: string,
  outputDir: string,
  options: CommonOptions
): Promise<any> {
  const url =
    base_url +
    'singleModeCompute?xpsfile=' +
    encodeURIComponent(xpsfile) +
    '&outputName=' +
    encodeURIComponent(outputName) +
    '&outputDir=' +
    encodeURIComponent(outputDir);

  return fetch(url, { method: 'post', body: JSON.stringify(options) })
    .then((r) => {
      return r.json();
    })
    .then((d) => {
      return d;
    })
    .catch((e) => console.log('Error: ' + e));
}

export async function multiModeCompute(
  xpsfiles: Array<string>,
  labels: Array<string>,
  outDir: string,
  outName: string,
  options: CommonOptions
): Promise<any> {
  const url = base_url + 'multiModeCompute';

  const options_schema = {
    multiInput: {
      xpsfiles: xpsfiles,
      labels: labels,
      outDir: outDir,
      outName: outName,
    },
    options: options,
  };

  return fetch(url, { method: 'post', body: JSON.stringify(options_schema) })
    .then((r) => {
      return r.json();
    })
    .then((d) => {
      return d;
    })
    .catch((e) => console.log('Error: ' + e));
}

export function open(path: string) {
  fetch(base_url + 'open/' + encodeURIComponent(path))
    .then((r) => {
      return r.json();
    })
    .catch((e) => {
      console.log('Error: ' + e);
    });
}

export function getDir(): Promise<{
  rootdir: string;
  basename: string;
  dirname: string;
}> {
  return fetch(base_url + 'getDir')
    .then((r) => {
      return r.json();
    })
    .catch((e) => {
      console.log('Error: ' + e);
      return null;
    });
}
