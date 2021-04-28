import React from 'react';

import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';

import FilesListItem from './FilesListItem';
import { Grid } from '@material-ui/core';

const FilesList = () => {
  const xps_files = useSelector((state: RootState) => state.app.xpsfiles);

  return (
    <Grid key="meu_amigo" item container xs={12}>
      {xps_files.map((file: string) => {
        return <FilesListItem file={file} />;
      })}
    </Grid>
  );
};

export default FilesList;
