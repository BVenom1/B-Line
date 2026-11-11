import React, { useState } from 'react';
import Signup from './signup';
import Login from './Login';

interface AccountManagerProps {
    signupPageToggleFunc?: React.Dispatch<React.SetStateAction<boolean>>
}

const AccountManager = ({ signupPageToggleFunc }: AccountManagerProps) => {

    const [loginToggle, setLoginToggle] = useState(false)

    const closeSignup = () => {
        if (signupPageToggleFunc != undefined) signupPageToggleFunc(false);
    }

    return (
        <div className="popup-overlay">
            <div className='popup-box'>
                <button className='btn circle-btn left-align' onClick={closeSignup}>x</button>
                {loginToggle ? <Login /> : <Signup />}
                <button className='btn t-btn left-align' onClick={() => setLoginToggle(p => !p)}>
                    {loginToggle ? "don't have an accout yet? Signup" : "have an account aleady? Login"}
                </button>
            </div>
        </div>
    )
}

export default AccountManager