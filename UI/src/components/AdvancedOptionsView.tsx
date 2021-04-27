import React from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Radio from '@material-ui/core/Radio';
import Typography from '@material-ui/core/Typography';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormLabel from '@material-ui/core/FormLabel';
import RadioGroup from '@material-ui/core/RadioGroup';
import Divider from '@material-ui/core/Divider';
import Switch from '@material-ui/core/Switch';
import Tooltip from '@material-ui/core/Tooltip';

// my imports
import useStyles from '../styles';
import InputSetOpen from './InputSetOpen';

const AdvancedOptionsView = () => {
  const classes = useStyles();
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
          <RadioGroup defaultValue="geo">
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
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Zeros à direita"
                type="number"
                required
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
          </Grid>
        </Grid>

        {/* <Grid item xs={12} className={classes.divider}>
          <Divider />
        </Grid> */}

        <Grid item container xs={12} justify={'flex-end'}>
          <Grid item>
            <Button variant="contained" color="secondary">
              Salvar configurações atuais
            </Button>
          </Grid>
        </Grid>
      </Grid>
    </>
  );
};

export default AdvancedOptionsView;
