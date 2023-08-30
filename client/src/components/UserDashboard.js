import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const UserDashboard = () => {
    const [user, setUser] = useState({});

    useEffect(() => {
        // Fetch the user details from the API
        fetch('/api/user')
            .then(response => response.json())
            .then(data => setUser(data))
            .catch(error => console.error(error));
    }, []);

    const handleLogout = () => {
        // Call your API to logout the user
    };
    return (
        <div>
            <div className="profile">
                <h2>Profile</h2>
                <p>Name: {user.name}</p>
                <p>Email: {user.email}</p>
                <button>Edit Profile</button>
            </div>
            <button onClick={handleLogout}>Logout</button>
            <div className="navigation-links">
                <Link to="/login">Login</Link>
                <Link to="/register">Register</Link>
            </div>
        </div>
    );
};

export default UserDashboard;
