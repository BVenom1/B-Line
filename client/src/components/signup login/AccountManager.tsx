import { useState } from 'react';
import Signup from './Signup';
import Login from './Login';

interface AccountManagerProps {
    accountManagerCloseFunc?: () => void;
}

const AccountManager = ({ accountManagerCloseFunc }: AccountManagerProps) => {

    const [loginToggle, setLoginToggle] = useState<"login" | "signup">("login")

    return (
        <div className="popup-overlay">
            <div className='popup-box'>
                <div className="row">
                    <h1 className='heading'>{loginToggle === "login" ? "Login" : "Signup"}</h1>
                    <div className="space"></div>
                    <button className='btn circle-btn right-align' onClick={accountManagerCloseFunc}>x</button>
                </div>
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
        </div >
    )
}

export default AccountManager