import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Provider } from 'react-redux';  // Import Provider from react-redux
import SignIn from './views/auth/signin';
import SignUp from './views/auth/signup'; 
import { JWTProvider } from './context/jwtcontext';
import store from './store/hidepassword';

function App() {
  return (
    <Provider store={store}>  {/* Wrap your application with Provider */}
      <Router>
        <JWTProvider>
          <div className="App">
            <Routes>
              <Route path="/signin" element={<SignIn />} />
              <Route path="/signup" element={<SignUp />} />
              <Route path="/" element={<SignIn />} /> 
            </Routes>
          </div>
        </JWTProvider>
      </Router>
    </Provider>
  );
}

export default App;
