import { Form, Input } from "semantic-ui-react";
import { Card } from "semantic-ui-react";
import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "./User";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function LoginForm() {

    const defaultCredentials = { username: '', password: '' }
    const [credentials, setCredentials] = useState(defaultCredentials);
    const { setUser } = useContext(UserContext);
    const [error, setError] = useState('');

    const history = useNavigate();

    const updateCredentials = e => {
        const { name, value } = e.target;
        setCredentials(prevCredentials => ({ ...prevCredentials, [name]: value }));
    }

    const handleLogin = async () => {
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(credentials)
            });

            if (response.status === 200) {
                const userData = await response.json();
                setUser(userData);
                toast.success('Logged in successfully!', {
                    position: toast.POSITION.TOP_CENTER,
                    autoClose: 2000,
                });
                history.push('/Home');
            } else if (response.status === 401) {
                setError('Incorrect password');
            } else if (response.status === 404) {
                setError('User not found');
            } else {
                const data = await response.json();
                setError(data.error || 'Failed to Login');
            }
        } catch (err) {
            setError('Unexpected Error Logging in, try again');
        }
    }

    return (
        <div>
            <Card>
                <h1>Service Center Login</h1>
                <Form onSubmit={handleLogin}>
                    <Form.Input>
                        <label>Username</label>
                        <Input
                            name='username'
                            onChange={updateCredentials}
                            type='text'
                            placeholder='Username'
                            value={credentials.username} />
                    </Form.Input>
                    <Form.Input>
                        <label>Password</label>
                        <Input
                            name='password'
                            type='password'
                            onChange={updateCredentials}
                            value={credentials.password}
                            placeholder='Password' />
                    </Form.Input>
                    <Form.Button>Sign In</Form.Button>
                </Form>
                {error && <div>{error}</div>}
                <ToastContainer />
            </Card>
        </div>
    )
}

export default LoginForm;
