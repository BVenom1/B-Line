import { useState } from "react";
import "./App.css";
import MainPage from "./components/main page/MainPage";
import AlertHandler from "./components/alerts/AlertHandler";
import { useGlobal } from "./GlobalContext";

function App() {
    const { addAlert } = useGlobal();

    const [count, setCount] = useState(0)

    const addMessage = () => {
        setCount(prev => prev + 1);
        addAlert(
            "Message",
            "This is a generic message " + count,
        );
    }

    return (
        <div>
            <h1>App</h1>
            <MainPage />
            <button className='btn t-btn' onClick={addMessage}>Add Message</button>
            <AlertHandler />
        </div>
    )

}

export default App;
