import React, { useEffect, useState } from 'react'
import { GroupModel, MembershipModel } from '../interfaces'
import { useGlobal } from '../../GlobalContext'

interface GroupPageProps {
    group: GroupModel,
    onReturnButtonClick: () => void
}

const GroupPage = ({ group, onReturnButtonClick }: GroupPageProps) => {
    const { user } = useGlobal();
    const [members, setMembers] = useState<MembershipModel[]>([]);

    useEffect(() => {
        if (user == undefined || user == null) return;
        fetch(`http://127.0.0.1:8000/user-${user.user_id}/group-${group.group_id}/get-group-members`)
            .then(res => {
                if (!res.ok) {
                    console.log(res.statusText);
                    throw new Error(res.statusText);
                }
                return res.json();
            })
            .then(res => {
                console.log(res);
                //setMembers(res);
            })
    }, [])

    return (
        <div className="grouppage">
            <div className="row">
                <div className="column">
                    <p className="no-margin">{user?.user_name}</p>
                    <p className="no-margin">{user?.email}</p>
                </div>
                <div className="column">
                    <p className="no-margin">{group.group_name}</p>
                    <p className="no-margin">{group.description}</p>
                </div>
            </div>
            <div className="column">{
                members.map(m => <div className="row">
                    <p>{m.user_id}</p>
                    <p>{m.membership_type}</p>
                </div>)
            }</div>
            <button className="btn" onClick={onReturnButtonClick}>Go back to main page</button>
        </div>
    )
}

export default GroupPage