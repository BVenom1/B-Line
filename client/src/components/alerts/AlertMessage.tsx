import React, { ReactNode } from 'react'
import { AlertModel } from '../interfaces'
import { useGlobal } from '../../GlobalContext'

const AlertMessage = ({ alert_id, style, children }: AlertModel) => {
    const { removeAlert } = useGlobal()

    return (
        <div className={"alert-box alert-" + style}>
            <div className="row">
                {style && <h3 className={"heading alert-heading-" + style}>{style}</h3>}
                <div className="space"></div>
                <button className='btn circle-btn right-align'
                    onClick={() => removeAlert(alert_id)}
                >x</button>
            </div>
            {children}
        </div>
    )
}

export default AlertMessage