import { useEffect, useState } from "react";
import { useGlobal } from "../../GlobalContext"
import AccountManager from "../signup login/AccountManager";
import Taskbar from "./Taskbar";
import { GroupModel, UserModel } from "../interfaces";
import GroupButton from "./GroupButton";

interface MainPageProps {
    onGroupButtonClick: (group: GroupModel) => void
}

const MainPage = ({ onGroupButtonClick }: MainPageProps) => {
    const { user, addAlert } = useGlobal();

    const [groups, setGroups] = useState<GroupModel[]>([])

    useEffect(() => {
        if (user == null || user == undefined) {
            setGroups([]);
            return;
        }
        try {
            fetch(`http://127.0.0.1:8000/user-${user.user_id}/get_groups`)
                .then(res => {
                    if (!res.ok) {
                        addAlert({
                            alert_id: "",
                            style: "Error",
                            children: res.statusText
                        });
                        throw new Error(res.statusText)
                    }
                    return res.json()
                })
                .then(resJSON => {
                    setGroups(resJSON)
                })
        } catch (e: unknown) {
            if (e instanceof Error) {
                console.error("Failed to fetch groups: ", e.message)
            } else {
                console.error("Unknown error when fetching groups: ", String(e))
            }
        }

    }, [user])

    return (
        <div className='main-page'>
            <Taskbar />
            {groups.map(g => <GroupButton group={g} onClick={() => onGroupButtonClick(g)} />)}
        </div>
    )
}

export default MainPage