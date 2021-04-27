import React from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
// import useStyles from '../styles';

// my imports
import * as controller from '../controller';

interface IProps {
  textLabel: string;
  setBtnLabel?: string;
  openBtnLabel?: string;
  // setIsPlotLog: React.Dispatch<React.SetStateAction<boolean>>;
}

const InputSetOpen = ({
  textLabel,
  setBtnLabel = '...',
  openBtnLabel = 'Abrir',
}: IProps) => {
  // const classes = useStyles();

  const handleSetClick = () => {
    console.log(controller.getXPSFiles());
  };

  const handleOpenClick = () => {
    console.log(controller.open('D:\\Desktop'));
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
            {setBtnLabel}
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
            {openBtnLabel}
          </Button>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default InputSetOpen;
