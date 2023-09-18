import React, { useState } from 'react';
import { Route, Switch, Redirect } from 'react-router-dom';
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
                          <li onClick={handleLogout} style={{...styles.link, ...styles.linkHover}}>Logout</li>
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

          <Switch>
              <Route exact path="/">
                  {isLoggedIn ? <UserDashboard user={user} /> : <Redirect to="/login" />}
              </Route>
              <Route path="/register">
                  {isLoggedIn ? <Redirect to="/" /> : <RegistrationForm />}
              </Route>
              <Route path="/login">
                  {isLoggedIn ? <Redirect to="/" /> : <LoginForm handleLogin={handleLogin} />}
              </Route>
          </Switch>
      </div>
  );
}

export default App;
