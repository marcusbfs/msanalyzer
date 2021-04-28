import React from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
// import useStyles from '../styles';
// redux
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';

// my imports
import * as controller from '../controller';
import { setOutDir } from '../redux/App.store';

interface IProps {
  textLabel: string;
}

const InputSetOpen = ({ textLabel }: IProps) => {
  // const classes = useStyles();

  const outDir = useSelector((state: RootState) => state.app.outDirName);
  const dispatch = useDispatch();

  const handleSetClick = () => {
    controller.getDir().then((d) => {
      dispatch(setOutDir(d.dirname));
    });
  };

  const handleOpenClick = () => {
    controller.open(outDir);
  };

  return (
    <Grid item container spacing={2}>
      <Grid
        item
        container
        xs={12}
        sm={10}
        alignItems="flex-end"
        justify="flex-start"
      >
        <Grid item xs>
          <TextField
            required
            value={outDir}
            InputProps={{
              readOnly: true,
            }}
            label={textLabel}
            fullWidth
          />
        </Grid>
      </Grid>
      <Grid
        item
        container
        xs={'auto'}
        sm={1}
        justify="flex-end"
        alignItems="flex-end"
      >
        <Grid item xs>
          <Button variant="contained" color="primary" onClick={handleSetClick}>
            ...
          </Button>
        </Grid>
      </Grid>
      <Grid
        item
        container
        xs={'auto'}
        sm={1}
        justify="flex-end"
        alignItems="flex-end"
      >
        <Grid item xs>
          <Button variant="contained" color="primary" onClick={handleOpenClick}>
            Abrir
          </Button>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default InputSetOpen;
