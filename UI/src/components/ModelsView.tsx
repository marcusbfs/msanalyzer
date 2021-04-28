import React from 'react';
import {
  Grid,
  Typography,
  Button,
  Divider,
  Select,
  MenuItem,
} from '@material-ui/core';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';

import * as controller from '../controller';

import { setCurrentModel } from '../redux/App.store';
import Image from './Image';

const ModelsView = () => {
  const dispatch = useDispatch();

  const basenames = useSelector((state: RootState) => state.app.basenames);
  const outName = useSelector((state: RootState) => state.app.outName);
  const outDir = useSelector((state: RootState) => state.app.outDirName);
  const currentModel = useSelector(
    (state: RootState) => state.app.currentModel
  );

  // functions
  const handleModelChange = (e) => {
    dispatch(setCurrentModel(e.target.value));
  };

  return (
    <Grid container item>
      <Grid
        item
        container
        xs={12}
        justify="center"
        style={{ marginBottom: '20px' }}
      >
        <Grid item>
          <Typography variant="h6">{basenames[0] + '.xps'} </Typography>
        </Grid>
      </Grid>

      <Grid container item xs={12}>
        <Grid
          container
          item
          alignItems="flex-end"
          style={{ marginBottom: '15px' }}
        >
          <Grid item xs={2}>
            <Typography variant="h6">Modelo: </Typography>
          </Grid>
          <Grid item xs={2}>
            <Select value={currentModel} onChange={handleModelChange}>
              <MenuItem value="RRB">RRB</MenuItem>
              <MenuItem value="Log-normal">Log-normal</MenuItem>
              <MenuItem value="Sigmoid">Sigmoid</MenuItem>
              <MenuItem value="GGS">GGS</MenuItem>
            </Select>
          </Grid>
          <Grid item container xs={8} justify="flex-end">
            <Grid item container xs={8} justify="flex-end">
              <Grid item>
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={() => {
                    controller.open(
                      outDir +
                        '\\' +
                        currentModel +
                        '_' +
                        outName +
                        '_model_parameters.txt'
                    );
                  }}
                  style={{ marginRight: '20px' }}
                >
                  Dados do modelo
                </Button>
              </Grid>
            </Grid>
            <Grid item xs={4}>
              <Button
                variant="contained"
                color="secondary"
                onClick={() => {
                  controller.open(
                    outDir + '\\' + outName + '_best_models_ranking.txt'
                  );
                }}
              >
                Ranking de modelos
              </Button>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={12}>
          <Divider />
        </Grid>
        <Grid item xs={12}>
          <Image
            image_source={
              outDir + '\\' + currentModel + '_' + outName + '_model.svg'
            }
          />
        </Grid>
      </Grid>
    </Grid>
  );
};

export default ModelsView;
