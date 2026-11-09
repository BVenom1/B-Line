import { useState } from "react";
import "./App.css";
import { UserModel } from "./components/interfaces";
import MainPage from "./components/main page/MainPage";

function App() {

    const [user, setUser] = useState<UserModel | null>(null)

    return (
        <div>
            <h1>App</h1>
            <MainPage user={{ user_name: "name" }} />
        </div>
    )

}

export default App;
