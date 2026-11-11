import React from 'react'

interface LoginProps {
    closeAccountManager?: () => void;
}

const Login = ({ closeAccountManager }: LoginProps) => {
    const onLogin = (event: React.SubmitEvent<HTMLFormElement>) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const formJSON = Object.fromEntries(formData.entries());
        console.log(formJSON);
        if (formJSON.uname_or_email == undefined || formJSON.uname_or_email === "") {
            //TODO: give alert for empty username
        }
        if (formJSON.password == undefined || formJSON.password === "") {
            //TODO: give alert for empty password
        }
        //TODO: send login request to server.
        closeAccountManager?.();
    }

    return (
        <div>
            <h1>Login</h1>
            <form className="form" onSubmit={onLogin}>
                <div className="form-row">
                    <label htmlFor="name">Username or Email</label>
                    <input type="text" id="uname_or_email" name="uname_or_email" placeholder="user_num_1" />
                </div>
                <div className="form-row">
                    <label htmlFor="password">Password</label>
                    <input type="password" name="password" id="login_password" />
                </div>
                <button type="submit" className='btn'>Login</button>
            </form>
        </div>
    )
}

export default Login