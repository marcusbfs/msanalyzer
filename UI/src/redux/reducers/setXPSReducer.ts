interface XPSStateType {
  xpsfiles: Array<string>;
}

const initialState: XPSStateType = { xpsfiles: [] };

export function setXPSReducer(
  state: XPSStateType = initialState,
  action: { type: string; payload: any }
) {
  // Check to see if the reducer cares about this action
  switch (action.type) {
    case 'setXPS':
      return {
        ...state,
        xpsfiles: action.payload,
      };
    default:
      return state;
  }
}

export default setXPSReducer;
