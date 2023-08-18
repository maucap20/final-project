import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

function LoginForm({ loginStatus, handleLogin }) {
  const history = useHistory();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState(null);

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.message === 'Login successful') {
          setLoginError(null);
          handleLogin(data);
          history.push(`/profile/${data.user_id}`);
        } else {
          setLoginError('Invalid username or password');
        }
      } else {
        setLoginError('Invalid username or password');
      }
    } catch (error) {
      console.error('Error logging in: ', error);
      setLoginError('An error occurred while logging in');
    }
  };

  return (
    <div>
      <div className="login-container">
        {loginError && <h2 className="login-error">{loginError}</h2>}
        <h1 className="log-in-header">Welcome Back</h1>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={handleUsernameChange}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={handlePasswordChange}
        />
        <button className="login-button" onClick={handleSubmit}>
          Log In
        </button>
      </div>
    </div>
  );
}

export default LoginForm;
