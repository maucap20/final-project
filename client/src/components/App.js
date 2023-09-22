import React, { useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import RegistrationForm from './RegistrationForm';
import UserDashboard from './UserDashboard';
import LoginForm from './LoginForm';


const styles = {
  nav: {
    backgroundColor: '#333',
    color: '#fff',
    padding: '10px 20px',
    display: 'flex',
    justifyContent: 'space-between'
  },
  navLinks: {
    listStyleType: 'none',
    padding: 0,
    display: 'flex',
    gap: '15px'
  },
  link: {
    textDecoration: 'none',
    color: '#fff'
  },
  error: {
    backgroundColor: 'red',
    color: '#fff',
    padding: '10px',
    borderRadius: '5px',
    margin: '10px 0',
    textAlign: 'center'
  }
};

function App() {

  const [user, setUser] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [error] = useState(null);


  const handleLogin = (userData) => {
    setUser(userData);
    setIsLoggedIn(true);
  };


  const handleLogout = () => {
    setUser(null);
    setIsLoggedIn(false);
  };


  return (
    <div style={styles.container}>
      <nav style={styles.nav}>
        <ul style={styles.navLinks}>
          {isLoggedIn ? (
            <>
              <li onClick={handleLogout} style={{ ...styles.link, ...styles.linkHover }}>Logout</li>
              <li><a href="/" style={styles.link}>Dashboard</a></li>
            </>
          ) : (
            <>
              <li><a href="/login" style={styles.link}>Login</a></li>
              <li><a href="/register" style={styles.link}>Register</a></li>
            </>
          )}
        </ul>
      </nav>

      {error && <div style={styles.error}>{error}</div>}

      <Routes>
          <Route path='/'></Route>
          {/* <Route path='/Home' element = {<Home />}></Route> */}
          {/* <Route path='/UserDashboard' element = {<UserDashboard />}></Route> */}
          <Route path='/register' element = {<RegistrationForm/>}></Route>
          <Route path='/login' element = {<LoginForm/>}></Route>
      </Routes>
    </div>
  );
}

export default App;
