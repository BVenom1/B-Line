import React, { useState } from 'react'
import { useGlobal } from '../../GlobalContext'
import AccountManager from '../signup login/AccountManager';

const Taskbar = () => {
    const { user, setUser } = useGlobal();

    const signout = () => setUser(null);

    const [accountManagerToggle, setAccountManagerToggle] = useState(false);

    return (
        <div className='task-bar row'>
            {
                user != undefined
                    ? <div className="column">
                        <div className="row left-align">
                            <h2 className="no-margin">{user.user_name}</h2>
                            <p className='no-margin right-align shadow-text'>{user.email}</p>
                        </div>
                        <p className="no-margin left-align shadow-text">{user.status}</p>
                    </div>
                    : <h3 className='no-margin left-align'>Please log in</h3>
            }
            <div className="space"></div>
            <div className="column">
                <button className='btn right-align' onClick={() => { setAccountManagerToggle(true) }}>{
                    user == undefined
                        ? "Log in"
                        : "Switch user"
                }</button>
                {
                    user != undefined
                        ? <button className="btn right-align" onClick={signout}>Log out</button>
                        : null
                }
            </div>
            {accountManagerToggle && <AccountManager accountManagerCloseFunc={() => setAccountManagerToggle(false)} />}
        </div>
    );
}

export default Taskbar;