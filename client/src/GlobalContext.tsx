import React, { createContext, ReactNode, useCallback, useContext, useState } from 'react'
import { AlertModel, UserModel } from "./components/interfaces"

interface GlobalContextType {
    theme: "light" | "dark",
    toggleTheme: () => void,
    user: UserModel | null,
    setUser: React.Dispatch<React.SetStateAction<UserModel | null>>,
    alerts: AlertModel[],
    addAlert: (alert: AlertModel, duration?: number) => string,
    removeAlert: (uuid: string) => void,
}

const GlobalContext = createContext<GlobalContextType | undefined>(undefined);

interface GlobalProviderProps {
    children: ReactNode,
}

// GlobalProvider react node as wrapper to provide global context
export const GlobalProvider = ({ children }: GlobalProviderProps) => {
    const [theme, setTheme] = useState<"light" | "dark">("dark")
    const [user, setUser] = useState<UserModel | null>(null)
    const toggleTheme = useCallback(() => {
        setTheme(prev => (prev === "dark" ? "light" : "dark"))
    }, [])

    const [alerts, setAlerts] = useState<AlertModel[]>([])
    const removeAlert = useCallback((uuid: string) => {
        setAlerts(prev => prev.filter(v => v.alert_id != uuid));
    }, [])
    const addAlert = useCallback((alert: AlertModel, duration: number = 3000) => {
        alert.alert_id = window.crypto.randomUUID();
        setAlerts(prev => [...prev, alert])
        setTimeout(() => {
            removeAlert(alert.alert_id)
        }, duration);

        return alert.alert_id;
    }, [removeAlert])

    return (
        <GlobalContext.Provider value={{
            theme, toggleTheme,
            user, setUser,
            alerts, addAlert, removeAlert
        }}>
            {children}
        </GlobalContext.Provider>
    )
}

// useGlobal hook to get variables from global context
export const useGlobal = (): GlobalContextType => {
    const context = useContext(GlobalContext);
    if (!context) throw new Error("useGlobal must be used within a GlobalProvider");
    return context;
}
