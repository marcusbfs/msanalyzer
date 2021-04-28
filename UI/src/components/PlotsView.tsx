import React from 'react';
import { Grid, Typography } from '@material-ui/core';
import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';

const PlotsView = () => {
  const dir = 'D:\\Desktop\\output\\resultados';
  const svg = dir + '\\NOME_BASE_curves.svg';

  const basenames = useSelector((state: RootState) => state.app.basenames);

  return (
    <Grid container item>
      <Grid item xs={2}>
        <Typography variant="h6">Arquivo: </Typography>
      </Grid>
      <Grid item container xs={10} justify="flex-start">
        <Grid item xs={12}>
          <Typography variant="h6">{basenames[0] + '.xps'} </Typography>
        </Grid>
      </Grid>
      <Grid item>
        <div>
          <img src={svg}></img>
        </div>
      </Grid>
    </Grid>
  );
};

export default PlotsView;
