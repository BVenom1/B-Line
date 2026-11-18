import React, { ReactNode } from 'react'

interface ErrorPageProps {
    children?: ReactNode,
    onReturnButtonClick: () => void
}

const ErrorPage = ({ children, onReturnButtonClick }: ErrorPageProps) => {
    return (
        <div className="error-page column">
            {children}
            <button className="btn left-align" onClick={onReturnButtonClick}>Return to Main Page</button>
        </div>
    )
}

export default ErrorPage