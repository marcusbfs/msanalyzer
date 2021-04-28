import React from 'react';
import { Grid, Typography, IconButton } from '@material-ui/core';
import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';
import LaunchIcon from '@material-ui/icons/Launch';

import * as controller from '../controller';

import CurvesPlot from './CurvesPlot';

const PlotsView = () => {
  const svg_file = useSelector((state: RootState) => state.app.singleSVGfile);

  return (
    <Grid container item>
      <Grid item container style={{ marginBottom: '30px' }}>
        <Grid item container xs={12} justify="center">
          <Grid item>
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
