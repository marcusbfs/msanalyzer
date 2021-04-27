import { configureStore } from '@reduxjs/toolkit';
import setXPSReducer from './reducers/setXPSReducer';
import setOutDirReducer from './reducers/setOutDirReducer';
import setOutNameReducer from './reducers/setOutNameReducer';

export const store = configureStore({
  reducer: {
    xps: setXPSReducer,
    outdir: setOutDirReducer,
    outname: setOutNameReducer,
  },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch;
