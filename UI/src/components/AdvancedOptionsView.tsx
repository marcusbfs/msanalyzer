import React from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Radio from '@material-ui/core/Radio';
import Typography from '@material-ui/core/Typography';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import SaveIcon from '@material-ui/icons/Save';
import RadioGroup from '@material-ui/core/RadioGroup';
import Divider from '@material-ui/core/Divider';
import Switch from '@material-ui/core/Switch';
import Tooltip from '@material-ui/core/Tooltip';
// redux
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';

// my imports
import useStyles from '../styles';
import {
  MeanType,
  setMeanType,
  toggleMultiLabel,
  setZerosRight,
  setZerosLeft,
} from '../redux/App.store';

const AdvancedOptionsView = () => {
  const classes = useStyles();

  const meanType = useSelector((state: RootState) => state.app.meanType);
  const multiLabel = useSelector((state: RootState) => state.app.multiLabel);
  const zerosLeft = useSelector((state: RootState) => state.app.zerosLeft);
  const zerosRight = useSelector((state: RootState) => state.app.zerosRight);
  const dispatch = useDispatch();

  return (
    <>
      <Grid item container>
        <Grid item container xs={12}>
          <Grid item>
            <Tooltip title="O manual do MasterSizer recomenda a utilização da média geométrica.">
              <Typography variant="h6">Tipo de média:</Typography>
            </Tooltip>
          </Grid>
        </Grid>
        <Grid item className={classes.typeDiaRadio}>
          <RadioGroup
            value={meanType === MeanType.geo ? 'geo' : 'ari'}
            onChange={(e) =>
              dispatch(
                setMeanType(
                  e.target.value === 'geo' ? MeanType.geo : MeanType.ari
                )
              )
            }
          >
            <FormControlLabel
              value="geo"
              control={<Radio color="primary" />}
              label="Geométrica"
              labelPlacement="end"
            />
            <FormControlLabel
              value="ari"
              control={<Radio color="primary" />}
              label="Aritimética"
              labelPlacement="end"
            />
          </RadioGroup>
        </Grid>
        <Grid item xs={12} className={classes.divider}>
          <Divider />
        </Grid>

        <Grid item xs>
          <FormControlLabel
            control={<Switch />}
            color="primary"
            label="Não colocar legendas nos gráficos de múltiplos arquivos"
            checked={multiLabel}
            onChange={() => dispatch(toggleMultiLabel())}
          />
        </Grid>

        <Grid item xs={12} className={classes.divider}>
          <Divider />
        </Grid>

        <Grid item container spacing={1}>
          <Grid container item xs={12}>
            <Grid item>
              <Tooltip title="Número de zeros a serem ignorados. Recomenda-se o menor valor possível; muitos zeros influenciam na otimização dos paramêtros do modelo.">
                <Typography variant="h6">Ignorar zeros:</Typography>
              </Tooltip>
            </Grid>
          </Grid>
          <Grid container item className={classes.ZerosIgnore} spacing={2}>
            <Grid item xs={12}>
              <TextField
                label="Zeros à esquerda"
                type="number"
                required
                value={zerosLeft}
                InputLabelProps={{
                  shrink: true,
                }}
                onChange={(e) => dispatch(setZerosLeft(Number(e.target.value)))}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Zeros à direita"
                type="number"
                required
                value={zerosRight}
                InputLabelProps={{
                  shrink: true,
                }}
                onChange={(e) =>
                  dispatch(setZerosRight(Number(e.target.value)))
                }
              />
            </Grid>
          </Grid>
        </Grid>

        {/* <Grid item xs={12} className={classes.divider}>
          <Divider />
        </Grid> */}

        <Grid item container xs={12} justify={'flex-end'}>
          <Grid item>
            <Button variant="contained" color="secondary" startIcon={<SaveIcon />}>
              Salvar configurações atuais
            </Button>
          </Grid>
        </Grid>
      </Grid>
    </>
  );
};

export default AdvancedOptionsView;
