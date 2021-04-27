import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import CssBaseline from '@material-ui/core/CssBaseline';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import Container from '@material-ui/core/Container';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';

// My custom
import useStyles from './styles';
import MainTabView from './components/MainTabView';
import AdvancedOptionsView from './components/AdvancedOptionsView';

const darkTheme = createMuiTheme({
  palette: {
    type: 'dark',
  },
});

const App = () => {
  const classes = useStyles();

  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const theme = React.useMemo(
    () =>
      createMuiTheme({
        palette: {
          type: prefersDarkMode ? 'dark' : 'light',
        },
      }),
    [prefersDarkMode]
  );

  // States
  const [tab, setTab] = React.useState(0);
  const [isPlotLog, setIsPlotLog] = React.useState(true);
  // const [xpsFiles, setIsPlotLog] = React.useState(true);

  return (
    <React.Fragment>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AppBar position="static" color="default" className={classes.appBar}>
          <Tabs
            value={tab}
            onChange={(e, v) => {
              setTab(v);
            }}
            variant="fullWidth"
          >
            <Tab label="Principal" />
            <Tab label="Opções avançadas" />
            <Tab label="Gráficos" />
            <Tab label="Modelos" />
          </Tabs>
        </AppBar>

        <main>
          <Container maxWidth="md" className={classes.mainTab}>
            {tab === 0 && (
              <Grid container>
                <MainTabView
                  isPlotLog={isPlotLog}
                  setIsPlotLog={setIsPlotLog}
                />
              </Grid>
            )}
            {tab === 1 && (
              <Grid container>
                <AdvancedOptionsView />
              </Grid>
            )}
            {tab === 2 && <Grid container>Gráficos</Grid>}
            {tab === 3 && <Grid container>Modelos</Grid>}

            <Grid container className={classes.execContainer}>
              <Grid item xs={12} className={classes.divider}>
                <Divider />
              </Grid>
              <Grid item container alignItems="flex-end" justify="flex-end">
                <Grid item xs>
                  <Button variant="contained" color="primary">
                    Executar
                  </Button>
                </Grid>
              </Grid>
            </Grid>
          </Container>
        </main>
      </ThemeProvider>
    </React.Fragment>
  );
};

export default App;
