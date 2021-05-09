import React from 'react';
import { render } from 'react-dom';
import App from './App';
import store from './redux/store';
import { Provider } from 'react-redux';
import { CssBaseline, createMuiTheme, ThemeProvider } from '@material-ui/core';

const darkTheme = createMuiTheme({
  palette: {
    type: 'dark',
  },
});

render(
  <React.StrictMode>
    <React.Fragment>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />

        <Provider store={store}>
          <App />
        </Provider>
      </ThemeProvider>
    </React.Fragment>
  </React.StrictMode>,

  document.getElementById('root')
);
