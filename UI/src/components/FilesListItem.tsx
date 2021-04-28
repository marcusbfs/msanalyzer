import React from 'react';

import ListItemText from '@material-ui/core/ListItemText';
import { Button, Grid } from '@material-ui/core';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';
import { setXPSFiles, setBasenames } from '../redux/App.store';

import * as controller from '../controller';

interface FilesListItemProps {
  file: string;
}

const FilesListItem = ({ file }: FilesListItemProps) => {
  const xpsfiles = useSelector((state: RootState) => state.app.xpsfiles);
  const basenames = useSelector((state: RootState) => state.app.basenames);
  const dispatch = useDispatch();

  // functions

  function handleClose() {
    var array = [...xpsfiles]; // make a separate copy of the array
    var brray = [...basenames]; // make a separate copy of the array
    var index = array.indexOf(file);
    if (index !== -1) {
      array.splice(index, 1);
      brray.splice(index, 1);
      dispatch(setXPSFiles(array));
      dispatch(setBasenames(brray));
    }
  }

  function handleOpen() {
    controller.open(file);
  }

  return (
    <>
      <Grid item container xs={12}>
        <Grid item container xs={8} justify="flex-start">
          <Grid item>
            <ListItemText primary={file} />
          </Grid>
        </Grid>
        <Grid item container xs={2} justify="flex-end">
          <Grid item>
            <Button variant="contained" color="secondary" onClick={handleClose}>
              X
            </Button>
          </Grid>
        </Grid>
        <Grid item container xs={2} justify="flex-end">
          <Grid item>
            <Button variant="contained" color="secondary" onClick={handleOpen}>
              Abrir
            </Button>
          </Grid>
        </Grid>
      </Grid>
    </>
  );
};

export default FilesListItem;
