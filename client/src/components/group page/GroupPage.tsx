import React from 'react'
import { GroupModel } from '../interfaces'
import { useGlobal } from '../../GlobalContext'

interface GroupPageProps {
    group: GroupModel,
    onReturnButtonClick: () => void
}

const GroupPage = ({ group, onReturnButtonClick }: GroupPageProps) => {
    const { user } = useGlobal();

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
            <button className="btn" onClick={onReturnButtonClick}>Go back to main page</button>
        </div>
    )
}

export default GroupPage