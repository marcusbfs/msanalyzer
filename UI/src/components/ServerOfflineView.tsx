import React from 'react';
import Container from '@material-ui/core/Container';

import useStyles from '../styles';
import { Typography, Grid } from '@material-ui/core';

const ServerOfflineView = () => {
  const classes = useStyles();
  return (
    <Container maxWidth="md" className={classes.mainTab}>
      <Grid container alignItems={'center'} justify={'center'}>
        <Typography>Servidor offline!</Typography>
      </Grid>
    </Container>
  );
};

export default ServerOfflineView;
