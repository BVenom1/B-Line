import React from 'react'
import AlertHandler from './components/alerts/AlertHandler'
import { useGlobal } from './GlobalContext'
import "./App.css";

const Test = () => {
    const { addAlert } = useGlobal();

    const addMessage = () => {
        addAlert(
            <p>This is a generic message</p>
            ,
            "Message"
        );
    }

    return (
        <div>
            <h1>Test</h1>
            <button className='btn t-btn' onClick={addMessage}>Add Message</button>
            <AlertHandler />
        </div>
    )
}

export default Test