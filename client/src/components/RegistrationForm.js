import React, { useState } from 'react';

function RegistrationForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = (event) => {
    event.preventDefault();

    if (!email || !password) {
        console.error('Email and password are required');
        return;
    }

    // if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
    //     console.error('Invalid email address');
    //     return;
    // }

    fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password,
        }),
    })
    .then(response => response.json().then(data => ({
        data: data,
        status: response.status,
    })))
    .then(res => {
        if (res.status === 200) {
            console.log(res.data);
            // handle success 
        } else {
            console.error(res.data);
            // handle error 
        }
    })
    .catch(error => {
        console.error('Error registering:', error);
    });
};


  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
      <input
        type= "text"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button >Register</button>
      </form>
    </div>
  );
}

export default RegistrationForm;
