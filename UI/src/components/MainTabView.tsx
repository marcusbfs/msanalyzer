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

// my imports
import useStyles from '../styles';
import InputSetOpen from './InputSetOpen';
import * as controller from '../controller';
import { setXPS } from '../redux/actions';
import { RootState } from '../redux/store';

interface IProps {
  isPlotLog: boolean;
  setIsPlotLog: React.Dispatch<React.SetStateAction<boolean>>;
}

const MainTabView = ({ isPlotLog, setIsPlotLog }: IProps) => {
  const classes = useStyles();

  const xps_files = useSelector((state: RootState) => state.xps.xpsfiles);
  const dispatch = useDispatch();

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
                onClick={() => {
                  controller.getXPSFiles().then((e) => {
                    dispatch(setXPS(e.files));
                  });
                }}
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
              <TextField required label="Nome de saída" fullWidth />
            </Grid>
          </Grid>
          <Grid
            container
            item
            xs={12}
            sm={1}
            // alignItems="flex-end"
            justify="flex-end"
          >
            <Grid item xs>
              <Button variant="contained" color="primary">
                Abrir
              </Button>
            </Grid>
          </Grid>
        </Grid>
        <Grid item>
          <FormControlLabel
            control={<Switch name="checked_log" />}
            color="primary"
            value={isPlotLog}
            onChange={() => {
              setIsPlotLog(!isPlotLog);
            }}
            label="Gráficos em escala logarítmica"
          />
        </Grid>
      </Grid>
    </>
  );
};

export default MainTabView;
