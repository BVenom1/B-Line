import React from 'react';
import { fetch } from '@tauri-apps/plugin-http';
import { useGlobal } from '../../GlobalContext';

interface SignupProps {
    goToLoginFunc?: () => void
}

const Signup = ({ goToLoginFunc }: SignupProps) => {

    const { addAlert } = useGlobal();

    const onSignup = async (event: React.SubmitEvent<HTMLFormElement>) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const formJSON = Object.fromEntries(formData.entries());
        console.log(formJSON);

        const res = await fetch("http://127.0.0.1:8000/signup", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ...formJSON })
        })

        const response = await res.json();

        if (!res.ok) addAlert({
            alert_id: "",
            style: "Error",
            children: response.detail
        });
        else {
            addAlert({
                alert_id: "",
                style: "Success",
                children: "Signup successful. Please log into your account"
            });
            goToLoginFunc?.();
        }
    }

    return (
        <div>
            <form className="form" onSubmit={onSignup}>
                <div className="row">
                    <label htmlFor="name">Username</label>
                    <input type="text" name='user_name' id='username' placeholder='username_1' />
                </div>
                <div className="row">
                    <label htmlFor="email">Email</label>
                    <input type="text" name='email' id='email' placeholder='user@example.com' />
                </div>
                <div className="row">
                    <label htmlFor="password">Password</label>
                    <input type="password" name='password' id='signup_password' />
                </div>
                <button type='submit' className='btn'>Signup</button>
            </form>
        </div>
    )
}

export default Signup