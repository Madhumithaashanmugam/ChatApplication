import React, { createContext, useEffect, useReducer } from 'react';
import {jwtDecode} from 'jwt-decode';  
import { ACCOUNT_INITIALISE, LOGIN, LOGOUT, SIGNUP } from '../store/action';
import axios from '../services/axios';
import { useNavigate } from 'react-router-dom';
import accountReducer from '../store/accountreducers';


const initialState = {
  isLoggedIn: false,
  isInitialised: false,
  user: null
};

const verifyToken = (access_token) => {
  if (!access_token) {
    return false;
  }

  const decoded = jwtDecode(access_token);
  return decoded.exp > Date.now() / 1000;
};

const setSession = (access_token) => {
  if (access_token) {
    localStorage.setItem('credentials', access_token);
    axios.defaults.headers.common.Authorization = `Bearer ${access_token}`;
  } else {
    localStorage.removeItem('credentials');
    delete axios.defaults.headers.common.Authorization;
  }
};

const JWTContext = createContext({
  ...initialState,
  login: () => {},
  logout: () => {},
  signup: () => {}
});

export const JWTProvider = ({ children }) => {
  const [state, dispatch] = useReducer(accountReducer, initialState);
  const navigate = useNavigate();  
  const login = async (email, password) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/account/signin', {
        username: email,
        password: password,
      });
      console.log('API Response:', response.data); // Log the full response
      const { access_token, user } = response.data;
      setSession(access_token);
      dispatch({
        type: LOGIN,
        payload: {
          user,
        },
      });
    } catch (error) {
      console.error('Signin error:', error.response ? error.response.data : error.message);
    }
  };
  const logout = () => {
    setSession(null);
    dispatch({ type: LOGOUT });
  };
  const signup = async (firstName, lastName, phoneNumber, email, password) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/account/login', {
        firstname: firstName,
        lastname: lastName,
        phone: phoneNumber,
        email,
        password,
        otherinfo: '',
      });
      const { access_token, user } = response.data;
      setSession(access_token);
      dispatch({
        type: SIGNUP,
        payload: {
          user,
        },
      });
      navigate('/signin');
    } catch (error) {
      console.error('Signup error:', error.response ? error.response.data : error.message);
    }
  };
  
  useEffect(() => {
    const init = async () => {
      try {
        const access_token = localStorage.getItem('credentials');
        if (access_token && verifyToken(access_token)) {
          setSession(access_token);
          const response = await axios.get('http://192.168.1.103:8000/users/me');
          const { user } = response.data;
          dispatch({
            type: ACCOUNT_INITIALISE,
            payload: {
              isLoggedIn: true,
              user
            }
          });
        } else {
          dispatch({
            type: ACCOUNT_INITIALISE,
            payload: {
              isLoggedIn: false,
              user: null
            }
          });
        }
      } catch (err) {
        console.error(err);
        dispatch({
          type: ACCOUNT_INITIALISE,
          payload: {
            isLoggedIn: false,
            user: null
          }
        });
      }
    };

    init();
  }, []);

  if (!state.isInitialised) {
    
    // return <Loader />;
    return <h1>Wait for some time</h1>;
  }

  return (
    <JWTContext.Provider value={{ ...state, login, logout, signup }}>
      {children}
    </JWTContext.Provider>
  );
};

export default JWTContext;
