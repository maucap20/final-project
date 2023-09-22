import React, { useContext, useState } from 'react';
import { useNavigate } from "react-router-dom";
import { UserContext } from './User';


function RegistrationForm() {
  const history = useNavigate();
  const [users, setUsers] = useState([])
  const [name, setName] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const {user, setUser} = useContext(UserContext)
  const [error, setError] = useState('')
  const [signUpError, setSignUpError] = useState("");


  const addUser = (newUser) => {
    setUsers([...users, newUser])
  }

  const newUser = { name: name, username: username, password: password }

  const handleSubmit = (event) => {
    event.preventDefault();
    handlePost(newUser);
  }

  function handlePost(newUser) {
    fetch('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newUser)
    })
      .then(r => {
        if (r.ok) {
          r.json().then(r_body => {
            setError('')
            setUser(r_body)

          })
        } else {
          r.json().then(message => setError(message.error))
        }
      })
      .then(newUser => addUser(newUser))

  };



  return (
    <div className='sign-up-parent-container'>
      <div className="sign-up-container">
        {signUpError && <h2 className="sign-up-error">{signUpError}</h2>}
        <h1 className="sign-up-header">Create an Account</h1>
        <form onSubmit={handleSubmit}>
          <input type="text" name="Name" placeholder="Name*" onChange={e=> setName(e.target.value)} />
          <input type="text" name="username" placeholder="Username/Email*" onChange={e=> setUsername(e.target.value)} />
          <input type="password" name="password" placeholder="Password*" onChange={e=> setPassword(e.target.value)} />
          <button className="sign-up-button" type="submit" onClick = {handleSubmit}>Submit</button>
        </form>
      </div>
    </div>
  );
}

export default RegistrationForm;
