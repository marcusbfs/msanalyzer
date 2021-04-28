import React from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Divider from '@material-ui/core/Divider';
import Switch from '@material-ui/core/Switch';
// redux
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';

// my imports
import useStyles from '../styles';
import InputSetOpen from './InputSetOpen';
import FilesList from './FilesList';
import * as controller from '../controller';
import {
  setOutDir,
  setOutName,
  setDirnames,
  setBasenames,
  setXPSFiles,
  toggleIsLogScale,
} from '../redux/App.store';

const MainTabView = () => {
  const classes = useStyles();

  const xps_files = useSelector((state: RootState) => state.app.xpsfiles);
  const basenames = useSelector((state: RootState) => state.app.basenames);
  const dirnames = useSelector((state: RootState) => state.app.dirnames);
  const outName = useSelector((state: RootState) => state.app.outName);
  const isLogScale = useSelector((state: RootState) => state.app.isLogScale);

  const dispatch = useDispatch();

  //functions

  const handleSetXPSFiles = () => {
    controller.getXPSFiles().then((e) => {
      dispatch(setBasenames(e.basenames));
      dispatch(setDirnames(e.dirnames));
      dispatch(setXPSFiles(e.files));
    });
  };

  React.useEffect(() => {
    if (xps_files.length > 0) {
      dispatch(setOutDir(dirnames[0]));
      dispatch(
        setOutName(xps_files.length > 1 ? 'arquivos_multiplos' : basenames[0])
      );
    } else {
      dispatch(setOutDir(''));
      dispatch(setOutName(''));
    }
  }, [xps_files]);

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
        <Grid item container xs={12}>
          <FilesList />
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

        <Grid item container alignItems="flex-end">
          <Grid item container xs={12}>
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
