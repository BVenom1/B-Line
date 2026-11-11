import React from 'react'
import { useGlobal } from '../../GlobalContext'
import AlertMessage from './AlertMessage';

const AlertHandler = () => {
    const { alerts, addAlert, removeAlert } = useGlobal();

    return (
        <div className='alert-handler'>
            {alerts.map(
                v => <AlertMessage alert_id={v.alert_id} style={v.style} children={v.children} />
            )}
        </div>
    )
}

export default AlertHandler