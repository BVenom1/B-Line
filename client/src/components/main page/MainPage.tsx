import { useEffect, useState } from "react";
import { useGlobal } from "../../GlobalContext"
import AccountManager from "../signup login/AccountManager";
import Taskbar from "./Taskbar";

const MainPage = () => {
    const { user } = useGlobal();

    useEffect(() => {
        //console.log("user changed", user)
        const getGroups = async () => {
            if (user == null || user == undefined) return;
            // TODO: fetch request for all the groups the user is part of
        }
        getGroups();
    }, [user])

    return (
        <div className='full-page'>
            <Taskbar />
        </div>
    )
}

export default MainPage