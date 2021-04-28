import React from 'react';

import ListItemText from '@material-ui/core/ListItemText';
import {
  Button,
  Grid,
  TextField,
  IconButton,
  Tooltip,
} from '@material-ui/core';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';
import { setXPSFiles, setBasenames } from '../redux/App.store';

import DeleteIcon from '@material-ui/icons/Delete';
import LaunchIcon from '@material-ui/icons/Launch';

import * as controller from '../controller';

import useStyles from '../styles';

interface FilesListItemProps {
  file: string;
}

const FilesListItem = ({ file }: FilesListItemProps) => {
  const classes = useStyles();

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
      <Grid item container xs={12} alignItems="center">
        <Grid item container xs={10} justify="flex-start">
          <Grid item xs={12} className={classes.fileItemText}>
            <TextField
              id="outlined-basic"
              value={file}
              variant="outlined"
              fullWidth
              InputProps={{
                readOnly: true,
              }}
            />
          </Grid>
        </Grid>
        <Grid item container xs={1} justify="flex-end">
          <Grid item xs={12}>
            <Tooltip title="Abrir">
              <IconButton onClick={handleOpen} color="secondary">
                <LaunchIcon />
              </IconButton>
            </Tooltip>
          </Grid>
        </Grid>
        <Grid item container xs={1} justify="flex-end">
          <Grid item xs={12}>
            <Tooltip title="Remover">
              <IconButton onClick={handleClose} color="secondary">
                <DeleteIcon />
              </IconButton>
            </Tooltip>
          </Grid>
        </Grid>
      </Grid>
    </>
  );
};

export default FilesListItem;
