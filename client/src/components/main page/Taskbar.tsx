import React, { useState } from 'react'
import { useGlobal } from '../../GlobalContext'
import AccountManager from '../signup login/AccountManager';

const Taskbar = () => {
    const { user, setUser } = useGlobal();

    const signout = () => setUser(null);

    const [accountManagerToggle, setAccountManagerToggle] = useState(false);

    return (
        <div className='taskbar row'>
            {
                user != undefined
                    ? <div className="column">
                        <h3 className="heading right-align">{user.user_name}</h3>
                        <p className='right-align'>{user.email}</p>
                    </div>
                    : <h3 className='heading right-align'>Please log in</h3>
            }
            <div className="space"></div>
            <div className="column gap">
                <button className='btn left-align' onClick={() => { setAccountManagerToggle(true) }}>{
                    user == undefined
                        ? "Log in"
                        : "Switch user"
                }</button>
                {
                    user != undefined
                        ? <button className="btn left-align" onClick={signout}>Log out</button>
                        : null
                }
            </div>
            {accountManagerToggle && <AccountManager accountManagerCloseFunc={() => setAccountManagerToggle(false)} />}
        </div>
    );
}

export default Taskbar;