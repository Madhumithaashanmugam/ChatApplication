import { ACCOUNT_INITIALISE,LOGIN, LOGOUT, SIGNUP } from "./action";
const accountReducer = (state, action) => {
    switch (action.type) {
      case ACCOUNT_INITIALISE: {
        //isLoggedIn and user is the properties of payload
        //  to create new users
        const { isLoggedIn, user } = action.payload;
        return {
          ...state,
          isLoggedIn,
          isInitialised: true,
          user
        };
      }
      //login to exitisting users
      case LOGIN: {
        const { user } = action.payload;
        return {
          ...state,
          isLoggedIn: true,
          user
        };
      }
      //for signup
      case SIGNUP:{
        const { user } = action.payload;
        return{  
          ...state,
          isLoggedIn: true,
          user
        };
      }
      //for logout
      case LOGOUT: {
        return {
          ...state,
          isLoggedIn: false,
          user: null
        };
      }

      default: {
        return { ...state };
      }
    }
  };
  
  export default accountReducer;
  
