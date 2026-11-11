import { useState } from "react";
import "./App.css";
import { UserModel } from "./components/interfaces";
import MainPage from "./components/main page/MainPage";
import AccountManager from "./components/signup login/AccountManager";

function App() {

    const [user, setUser] = useState<UserModel | null>(null)
    const [toggleSignup, setToggleSignup] = useState(true)

    return (
        <div>
            <h1>App</h1>
            <MainPage signupPageToggleFunc={setToggleSignup} />
            {toggleSignup && <AccountManager signupPageToggleFunc={setToggleSignup} />}
        </div>
    )

}

export default App;
