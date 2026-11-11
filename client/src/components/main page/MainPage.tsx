import { useState } from "react";
import { useGlobal } from "../../GlobalContext"
import AccountManager from "../signup login/AccountManager";

const MainPage = () => {
    const { user } = useGlobal();

    const [accountManagerToggle, setAccountManagerToggle] = useState(false)

    return (
        <div className='full-page'>
            <h1>Main Page</h1>
            {(user == undefined)
                ? <p>user is not logged in</p>
                : <p>user {user.user_name} is logged in</p>
            }
            <button className='btn t-btn' onClick={() => { setAccountManagerToggle(true) }}>Sign up</button>
            {accountManagerToggle && <AccountManager accountManagerCloseFunc={() => setAccountManagerToggle(false)} />}
        </div>
    )
}

export default MainPage