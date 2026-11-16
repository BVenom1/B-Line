import React from 'react'
import { GroupModel } from '../interfaces'

const GroupButton = (group: GroupModel) => {
    return (
        <div className="group-button row">
            <div className="column">
                <h3 className="heading left-align">{group.group_name}</h3>
                <p className="left-align">{group.description}</p>
            </div>
            <div className="space"></div>
            <div className="right-align">{
                group.created_at?.getFullYear() + "-" +
                group.created_at?.getMonth() + "-" +
                group.created_at?.getDate()
            }</div>
        </div>
    )
}

export default GroupButton