import { createStore } from 'redux';

const initialState = {
  passwordVisible: false,
};

const TOGGLE_PASSWORD_VISIBILITY = 'TOGGLE_PASSWORD_VISIBILITY';

export const togglePasswordVisibility = () => ({
  type: TOGGLE_PASSWORD_VISIBILITY,
});

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case TOGGLE_PASSWORD_VISIBILITY:
      return {
        ...state,
        passwordVisible: !state.passwordVisible,
      };
    default:
      return state;
  }
};

const store = createStore(reducer);

export default store;
