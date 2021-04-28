import React from 'react';
import List from '@material-ui/core/List';

import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';

import FilesListItem from './FilesListItem';
import { ListItem, Grid } from '@material-ui/core';

const FilesList = () => {
  const xps_files = useSelector((state: RootState) => state.app.xpsfiles);

  return (
    <Grid container>
      <List component="ul" disablePadding>
        {xps_files.map((file: string) => {
          return (
            <ListItem key={file} disableGutters>
              <FilesListItem file={file} />
            </ListItem>
          );
        })}
      </List>
    </Grid>
  );
};

export default FilesList;
