import React from 'react'
import { fetch } from '@tauri-apps/plugin-http';
import { useGlobal } from '../../GlobalContext';

interface LoginProps {
    closeAccountManager?: () => void;
}

const Login = ({ closeAccountManager }: LoginProps) => {

    const { addAlert, setUser } = useGlobal()


    const onLogin = async (event: React.SubmitEvent<HTMLFormElement>) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const formJSON = Object.fromEntries(formData.entries());
        if (formJSON.uname_or_email == undefined || formJSON.uname_or_email === "") {
            addAlert({
                alert_id: "",
                style: "Error",
                children: "Please enter a username or email."
            })
        }
        if (formJSON.password == undefined || formJSON.password === "") {
            addAlert({
                alert_id: "",
                style: "Error",
                children: "Please enter a password."
            })
        }

        const res = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formJSON)
        });

        const response = await res.json()

        if (!res.ok) addAlert({
            alert_id: "",
            style: "Error",
            children: response.detail
        });
        else {
            setUser(response);
            addAlert({
                alert_id: "",
                style: "Success",
                children: "You have successfully logged in"
            });
            closeAccountManager?.();
        }
    }

    return (
        <div>
            <form className="form" onSubmit={onLogin}>
                <div className="row">
                    <label htmlFor="name">Username or Email</label>
                    <input type="text" id="uname_or_email" name="uname_or_email" placeholder="user_num_1" />
                </div>
                <div className="row">
                    <label htmlFor="password">Password</label>
                    <input type="password" name="password" id="login_password" />
                </div>
                <button type="submit" className='btn'>Login</button>
            </form>
        </div>
    )
}

export default Login