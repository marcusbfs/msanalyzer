import React from 'react';
import List from '@material-ui/core/List';

import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';

import FilesListItem from './FilesListItem';
import { ListItem, Grid } from '@material-ui/core';

const FilesList = () => {
  const xps_files = useSelector((state: RootState) => state.app.xpsfiles);

  return (
    <Grid item container xs={12}>
      {xps_files.map((file: string) => {
        return <FilesListItem file={file} />;
      })}
    </Grid>
  );
};

export default FilesList;
