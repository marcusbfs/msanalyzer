import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';

const App = () => {
  const [tab, setTab] = React.useState(0);

  return (
    <Container>
      <AppBar position="static" color="default">
        <Tabs
          value={tab}
          onChange={(e, v) => {
            setTab(v);
          }}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
        >
          <Tab label="Principal" />
          <Tab label="Tab 2" />
          <Tab label="Tab 3" />
        </Tabs>
      </AppBar>

      {tab === 0 && <Grid container>Tab 0</Grid>}
      {tab === 1 && <Grid container>Tab 1</Grid>}
      {tab === 2 && <Grid container>Tab 2</Grid>}
    </Container>
  );
};

export default App;
