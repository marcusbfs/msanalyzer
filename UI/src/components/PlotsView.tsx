import React from 'react';
import {
  Grid,
  Typography,
  Container,
  Button,
  IconButton,
} from '@material-ui/core';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';
import LaunchIcon from '@material-ui/icons/Launch';

import useStyles from '../styles';
import * as controller from '../controller';

import { setSingleSVGfile } from '../redux/App.store';
import CurvesPlot from './CurvesPlot';

const PlotsView = () => {
  const classes = useStyles();

  const dispatch = useDispatch();

  const xpsfiles = useSelector((state: RootState) => state.app.xpsfiles);
  const basenames = useSelector((state: RootState) => state.app.basenames);
  const meanType = useSelector((state: RootState) => state.app.meanType);
  const zerosLeft = useSelector((state: RootState) => state.app.zerosLeft);
  const zerosRight = useSelector((state: RootState) => state.app.zerosRight);
  const isLogScale = useSelector((state: RootState) => state.app.isLogScale);
  const isComputing = useSelector((state: RootState) => state.app.isComputing);
  const outName = useSelector((state: RootState) => state.app.outName);
  const outDir = useSelector((state: RootState) => state.app.outDirName);
  const svg_file = useSelector((state: RootState) => state.app.singleSVGfile);

  return (
    <Grid container item>
      <Grid item container style={{ marginBottom: '30px' }}>
        <Grid item xs={2}>
          <Typography variant="h6">Arquivo: </Typography>
        </Grid>
        <Grid item container xs={10} justify="flex-start">
          <Grid item xs={12}>
            <Typography variant="h6">{svg_file} </Typography>
          </Grid>
        </Grid>
      </Grid>
      <Grid item xs={12}>
        <CurvesPlot />
      </Grid>
      <Grid item container xs={12} justify="flex-end">
        <Grid item>
          <IconButton
            onClick={() => controller.open(svg_file)}
            color="secondary"
          >
            <LaunchIcon />
          </IconButton>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default PlotsView;
