import React from 'react';

interface SignupProps {
    goToLoginFunc?: () => void
}

const Signup = ({ goToLoginFunc }: SignupProps) => {
    const onSignup = (event: React.SubmitEvent<HTMLFormElement>) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const formJSON = Object.fromEntries(formData.entries());
        console.log(formJSON);
        //TODO: send signup request to server
        goToLoginFunc?.();
    }

    return (
        <div>
            <h1>Signup</h1>
            <form className="form" onSubmit={onSignup}>
                <div className="form-row">
                    <label htmlFor="name">Username</label>
                    <input type="text" name='username' id='username' placeholder='username_1' />
                </div>
                <div className="form-row">
                    <label htmlFor="email">Email</label>
                    <input type="text" name='email' id='email' placeholder='user@example.com' />
                </div>
                <div className="form-row">
                    <label htmlFor="password">Password</label>
                    <input type="password" name='password' id='signup_password' />
                </div>
                <button type='submit' className='btn'>Signup</button>
            </form>
        </div>
    )
}

export default Signup