import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import CircularProgress from '@material-ui/core/CircularProgress';

import { useDispatch, useSelector } from 'react-redux';

// My custom
import useStyles from './styles';
import MainTabView from './components/MainTabView';
import ServerOfflineView from './components/ServerOfflineView';
import PlotsView from './components/PlotsView';
import ModelsView from './components/ModelsView';
import AdvancedOptionsView from './components/AdvancedOptionsView';
import { RootState } from './redux/store';
import {
  setIsSingleFile,
  MeanType,
  setIsSpinnerHidden,
  setIsComputing,
  setIsServerOn,
  setIsXPSEmpty,
  setMeanType,
  setZerosRight,
  setZerosLeft,
} from './redux/App.store';
import * as controller from './controller';

const App = () => {
  const classes = useStyles();

  // States
  const dispatch = useDispatch();
  const [tab, setTab] = React.useState(0);
  const isSpinnerHidden = useSelector(
    (state: RootState) => state.app.isSpinnerHidden
  );
  const xpsfiles = useSelector((state: RootState) => state.app.xpsfiles);
  const basenames = useSelector((state: RootState) => state.app.basenames);
  const meanType = useSelector((state: RootState) => state.app.meanType);
  const zerosLeft = useSelector((state: RootState) => state.app.zerosLeft);
  const zerosRight = useSelector((state: RootState) => state.app.zerosRight);
  const isLogScale = useSelector((state: RootState) => state.app.isLogScale);
  const outName = useSelector((state: RootState) => state.app.outName);
  const outDir = useSelector((state: RootState) => state.app.outDirName);
  const isComputing = useSelector((state: RootState) => state.app.isComputing);
  const multiLabel = useSelector((state: RootState) => state.app.multiLabel);
  const isServerOn = useSelector((state: RootState) => state.app.isServerOn);
  const isXPSEmpty = useSelector((state: RootState) => state.app.isXPSEmpty);
  const isSingleFile = useSelector(
    (state: RootState) => state.app.isSingleFile
  );

  // use effects
  React.useEffect(() => {
    dispatch(setIsSingleFile(xpsfiles.length <= 1));
  }, [xpsfiles]);

  let path = require('path');
  let pyProc: any = null;
  const app = require('electron').remote.app;
  let api_exe_path: string = path.join(
    path.dirname(app.getAppPath()),
    '..',
    'msanalyzer_api',
    'local_api.exe'
  );

  const exitPyProc = () => {
    console.log('Exiting Python process');
    if (pyProc) {
      pyProc.kill();
    }
    pyProc = null;
  };

  const callPythonServer = () => {
    let fs = require('fs');
    // initialize python server
    if (fs.existsSync('../msanalyzer/local_api.py')) {
      console.log('Dev mode');
    } else {
      console.log('Dist mode');
      console.log('Starting Python process');
      // pyProc = require('child_process').execFile(api_exe_path);
    }
  };

  const startServer = () => {
    // check if its alive first
    controller
      .isAlive()
      .then((d) => {
        // Server is alive: do nothing
        console.log('Server is already online');
        return;
      })
      .catch((e) => {
        // Server is not alive: start server
        console.log('Server offline: calling python');
        callPythonServer();
      });
  };

  // Use effects

  React.useEffect(() => {
    if (isServerOn) {
      // controller
      //   .getConfig()
      //   .then((options) => {
      //     dispatch(
      //       setMeanType(
      //         options.meanType === 'geo' ? MeanType.geo : MeanType.ari
      //       )
      //     );
      //     dispatch(setZerosRight(options.zerosRight));
      //     dispatch(setZerosLeft(options.zerosLeft));
      //   })
      //   .catch((e) => {
      //     console.log('Error: ' + e);
      //   });
    }
  }, []);

  React.useEffect(() => {
    startServer();
    return () => {
      exitPyProc();
    };
  }, []);

  React.useEffect(() => {
    dispatch(setIsXPSEmpty(xpsfiles.length < 1));
  }, [xpsfiles]);

  const INTERVAL_MS = 5000;

  React.useEffect(() => {
    const interval = setInterval(() => {
      controller
        .isAlive()
        .then((d) => {
          dispatch(setIsServerOn(true));
        })
        .catch((e) => {
          dispatch(setIsServerOn(false));
          console.log('Error: ' + e);
        });
    }, INTERVAL_MS);

    return () => clearInterval(interval); // This represents the unmount function, in which you need to clear your interval to prevent memory leaks.
  }, []);

  // functions

  function handleExecSingle() {
    const options: controller.CommonOptions = {
      meanType: meanType === MeanType.geo ? 'geo' : 'ari',
      zerosLeft: zerosLeft,
      zerosRight: zerosRight,
      logScale: isLogScale,
      multiLabel: multiLabel,
    };
    controller
      .singleModeCompute(xpsfiles[0], outName, outDir, options)
      .then()
      .catch((e) => {
        console.log('Error in single: ' + e);
      })
      .finally(() => {
        // useForceUpdate();
        dispatch(setIsSpinnerHidden(true));
        dispatch(setIsComputing(false));
      });
  }

  function handleExecMulti() {
    const options: controller.CommonOptions = {
      meanType: meanType === MeanType.geo ? 'geo' : 'ari',
      zerosLeft: zerosLeft,
      zerosRight: zerosRight,
      logScale: isLogScale,
      multiLabel: multiLabel,
    };

    controller
      .multiModeCompute(xpsfiles, basenames, outDir, outName, options)
      .then()
      .catch((e) => {
        console.log('Error: ' + e);
      })
      .finally(() => {
        dispatch(setIsSpinnerHidden(true));
        dispatch(setIsComputing(false));
      });
  }

  function handleExec() {
    dispatch(setIsSpinnerHidden(false));
    dispatch(setIsComputing(true));
    if (isSingleFile) {
      return handleExecSingle();
    } else {
      return handleExecMulti();
    }
  }

  return (
    <React.Fragment>
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
          <Tab label="Curvas" disabled={isXPSEmpty} />
          <Tab label="Modelos" disabled={isXPSEmpty || !isSingleFile} />
        </Tabs>
      </AppBar>

      <main>
        {isServerOn ? (
          <Container maxWidth="md" className={classes.mainTab}>
            <Grid
              container
              direction="column"
              justify="space-between"
              alignItems="center"
            >
              <Grid item container>
                {tab === 0 && <MainTabView />}
                {tab === 1 && <AdvancedOptionsView />}
                {tab === 2 && <PlotsView />}
                {tab === 3 && <ModelsView />}
              </Grid>

              <Grid item container className={classes.execContainer}>
                <Grid item xs={12} className={classes.divider}>
                  <Divider />
                </Grid>
                <Grid item container alignItems="flex-end">
                  <Grid item xs={3}>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={handleExec}
                      disabled={isComputing || isXPSEmpty}
                    >
                      Executar
                    </Button>
                  </Grid>
                  <Grid item container xs={9} justify="flex-end">
                    {!isSpinnerHidden && (
                      <Grid item>
                        <CircularProgress color="secondary" />
                      </Grid>
                    )}
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </Container>
        ) : (
          <div>
            <ServerOfflineView api_exe_path={api_exe_path} />
          </div>
        )}
      </main>
    </React.Fragment>
  );
};

export default App;
