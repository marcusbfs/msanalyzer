import React from 'react';
import Container from '@material-ui/core/Container';

import useStyles from '../styles';
import { Typography, Grid } from '@material-ui/core';

interface PropsTypes {
  api_exe_path: string;
}

const ServerOfflineView = ({ api_exe_path }: PropsTypes) => {
  const classes = useStyles();
  return (
    <Container maxWidth="md" className={classes.mainTab}>
      <Grid container alignItems={'center'} justify={'center'}>
        <Grid item>
          <Typography variant="h1">Servidor offline!</Typography>
        </Grid>
        <Grid item xs={12}>
          <Grid item>
            <Typography variant="h5">
              Verifique se há algo de errado em {api_exe_path}
            </Typography>
          </Grid>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ServerOfflineView;
