import React, { createContext, ReactNode, useContext, useState } from 'react'
import { UserModel } from "./components/interfaces"

interface GlobalContextType {
    theme: "light" | "dark",
    toggleTheme: () => void,
    user: UserModel | null
    setUser: React.Dispatch<React.SetStateAction<UserModel | null>>
}

const GlobalContext = createContext<GlobalContextType | undefined>(undefined);

interface GlobalProviderProps {
    children: ReactNode,
}

// GlobalProvider react node as wrapper to provide global context
export const GlobalProvider = ({ children }: GlobalProviderProps) => {
    const [theme, setTheme] = useState<"light" | "dark">("dark")
    const [user, setUser] = useState<UserModel | null>(null)
    const toggleTheme = () => {
        setTheme(prev => (prev === "dark" ? "light" : "dark"))
    }

    return (
        <GlobalContext.Provider value={{ theme, toggleTheme, user, setUser }}>
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
