const base_url = 'http://127.0.0.1:2342/';

export function getXPSFiles() {
  const options = {
    fileTypes: [['Arquivos XPS', '.xps']],
  };

  fetch(base_url + 'getFiles', {
    method: 'post',
    body: JSON.stringify(options),
  })
    .then((r) => {
      return r.json();
    })
    .then((d) => {
      return d;
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
