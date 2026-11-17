import React from 'react'
import { GroupModel } from '../interfaces'

interface GroupButtonProps {
    group: GroupModel
}

const GroupButton = ({ group }: GroupButtonProps) => {
    return (
        <div className="groupbutton row">
            <div className="column">
                <h3 className="no-margin left-align">{group.group_name}</h3>
                <p className="no-margin left-align shadow-text">{group.description}</p>
            </div>
            <div className="space"></div>
            <div className='shadow-text'>{String(group.created_at).slice(0, 10)}</div>
        </div>
    )
}

export default GroupButton