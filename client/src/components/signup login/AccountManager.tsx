import { useState } from 'react';
import Signup from './signup';
import Login from './Login';

interface AccountManagerProps {
    accountManagerCloseFunc?: () => void;
}

const AccountManager = ({ accountManagerCloseFunc }: AccountManagerProps) => {

    const [loginToggle, setLoginToggle] = useState<"login" | "signup">("login")

    return (
        <div className="popup-overlay">
            <div className='popup-box'>
                <button className='btn circle-btn left-align' onClick={accountManagerCloseFunc}>x</button>
                {loginToggle === "login"
                    ? <Login closeAccountManager={accountManagerCloseFunc} />
                    : <Signup goToLoginFunc={() => setLoginToggle("login")} />
                }
                <button className='btn t-btn left-align' onClick={
                    () => setLoginToggle(p => p === "login" ? "signup" : "login")
                }>
                    {loginToggle === "login" ? "don't have an accout yet? Signup" : "have an account aleady? Login"}
                </button>
            </div>
        </div>
    )
}

export default AccountManager