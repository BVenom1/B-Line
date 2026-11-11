import { UserModel } from '../interfaces'

interface MainPageProps {
    user?: UserModel,
    signupPageToggleFunc?: React.Dispatch<React.SetStateAction<boolean>>
}

const MainPage = ({ user, signupPageToggleFunc }: MainPageProps) => {
    const toggleSignup = () => {
        if (signupPageToggleFunc != undefined) signupPageToggleFunc(prev => !prev);
    }

    return (
        <div className='full-page'>
            <h1>Main Page</h1>
            {(user == undefined)
                ? <p>user is not logged in</p>
                : <p>user {user.user_name} is logged in</p>
            }
            <button className='btn t-btn' onClick={toggleSignup}>Sign up</button>
        </div>
    )
}

export default MainPage