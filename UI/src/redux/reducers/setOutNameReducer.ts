interface OutNameType {
  outname: string;
}

const initialState: OutNameType = { outname: '' };

export function setOutNameReducer(
  state: OutNameType = initialState,
  action: { type: string; payload: any }
) {
  // Check to see if the reducer cares about this action
  switch (action.type) {
    case 'setOutName':
      return {
        ...state,
        outname: action.payload,
      };
    default:
      return state;
  }
}

export default setOutNameReducer;
