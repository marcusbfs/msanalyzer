import React from 'react';

import { Grid, TextField, IconButton, Tooltip } from '@material-ui/core';
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
    <Grid item container xs={12} key={file} alignItems="center">
      <Grid item container xs={10} key={file + '_1'} justify="flex-start">
        <Grid item xs={12} key={file + '_2'} className={classes.fileItemText}>
          <TextField
            id="outlined-basic"
            value={file}
            variant="outlined"
            fullWidth
            InputProps={{
              readOnly: true,
            }}
            key={file + '_txt'}
          />
        </Grid>
      </Grid>
      <Grid item container xs={1} key={file + '_3'} justify="flex-end">
        <Grid item xs={12} key={file + '_4'}>
          <Tooltip title="Abrir" key={file + '_tooltip1'}>
            <IconButton
              onClick={handleOpen}
              color="secondary"
              key={file + '_button1'}
            >
              <LaunchIcon key={file + '_icon1'} />
            </IconButton>
          </Tooltip>
        </Grid>
      </Grid>
      <Grid item container xs={1} justify="flex-end" key={file + '_5'}>
        <Grid item xs={12} key={file + '_6'}>
          <Tooltip title="Remover" key={file + '_tooltip2'}>
            <IconButton
              onClick={handleClose}
              color="secondary"
              key={file + '_button2'}
            >
              <DeleteIcon key={file + '_icon2'} />
            </IconButton>
          </Tooltip>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default FilesListItem;
