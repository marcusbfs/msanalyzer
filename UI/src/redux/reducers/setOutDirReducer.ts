interface OutDirStateType {
  outdir: string;
}

const initialState: OutDirStateType = { outdir: '' };

export function setOutDirReducer(
  state: OutDirStateType = initialState,
  action: { type: string; payload: any }
) {
  // Check to see if the reducer cares about this action
  switch (action.type) {
    case 'setOutDir':
      return {
        ...state,
        outdir: action.payload,
      };
    default:
      return state;
  }
}

export default setOutDirReducer;
