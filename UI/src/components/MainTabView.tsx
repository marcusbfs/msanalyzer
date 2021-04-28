import React from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Divider from '@material-ui/core/Divider';
import Switch from '@material-ui/core/Switch';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
// redux
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';

// my imports
import useStyles from '../styles';
import InputSetOpen from './InputSetOpen';
import * as controller from '../controller';
import {
  setOutDir,
  setOutName,
  setXPSFiles,
  toggleIsLogScale,
} from '../redux/App.store';

const MainTabView = () => {
  const classes = useStyles();

  const xps_files = useSelector((state: RootState) => state.app.xpsfiles);
  const outName = useSelector((state: RootState) => state.app.outName);
  const isLogScale = useSelector((state: RootState) => state.app.isLogScale);

  const dispatch = useDispatch();

  //functions

  const handleSetXPSFiles = () => {
    controller.getXPSFiles().then((e) => {
      dispatch(setXPSFiles(e.files));
      if (e.files.length > 0) {
        dispatch(setOutDir(e.dirnames[0]));
        dispatch(
          setOutName(e.files.length > 1 ? 'arquivos_multiplos' : e.basenames[0])
        );
      } else {
        dispatch(setOutDir(''));
        dispatch(setOutName(''));
      }
    });
  };

  return (
    <>
      {/* <InputSetOpen textLabel="Arquivo(s) XPS" /> */}
      <Grid container spacing={2}>
        <Grid item container>
          <Grid item sm={9}>
            <Typography variant="h5">Arquivo(s) XPS</Typography>
          </Grid>
          <Grid item container sm={3} justify="flex-end">
            <Grid item>
              <Button
                variant="contained"
                color="primary"
                onClick={handleSetXPSFiles}
              >
                Selecionar
              </Button>
            </Grid>
          </Grid>
        </Grid>
        <Grid item>
          <List component="ul">
            {xps_files.map((file: string) => {
              return (
                <ListItem key={file} alignItems="flex-start">
                  <ListItemText primary={file} />
                </ListItem>
              );
            })}
          </List>
        </Grid>
      </Grid>

      <Grid container className={classes.divider}>
        <Grid item xs={12}>
          <Divider />
        </Grid>
      </Grid>

      <Grid container spacing={3} className={classes.mainTabOptions}>
        <Grid item container xs={12} alignItems="flex-end" justify="flex-start">
          <Grid item xs>
            <Typography variant="h5"> Opções</Typography>
          </Grid>
        </Grid>

        <InputSetOpen textLabel="Diretório de saída" />

        <Grid item container alignItems="flex-end" spacing={2}>
          <Grid item container xs={12} sm={11}>
            <Grid item xs>
              <TextField
                required
                label="Nome de saída"
                fullWidth
                value={outName}
                onChange={(e) => {
                  dispatch(setOutName(e.target.value));
                }}
              />
            </Grid>
          </Grid>
          {/* <Grid container item xs={12} sm={1} justify="flex-end">
            <Grid item xs>
              <Button
                variant="contained"
                color="primary"
                onClick={() => controller.open(outDir + '\\' + outName)}
              >
                Abrir
              </Button>
            </Grid>
          </Grid> */}
        </Grid>
        <Grid item>
          <FormControlLabel
            control={<Switch name="checked_log" />}
            color="primary"
            checked={isLogScale}
            onChange={() => {
              dispatch(toggleIsLogScale());
            }}
            label="Gráficos em escala logarítmica"
          />
        </Grid>
      </Grid>
    </>
  );
};

export default MainTabView;
