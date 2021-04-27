const base_url = 'http://127.0.0.1:2342/';

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

export function open(path: string) {
  fetch(base_url + 'open/' + encodeURIComponent(path))
    .then((r) => {
      return r.json();
    })
    .catch((e) => {
      console.log('Error: ' + e);
    });
}
