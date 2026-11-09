import { UserModel } from '../interfaces'

interface MainPageProps {
    user?: UserModel,
}

const MainPage = ({ user }: MainPageProps) => {
    return (
        <div>
            <h1>Main Page</h1>
            {(user == undefined)
                ? <p>user is not logged in</p>
                : <p>user {user.user_name} is logged in</p>
            }
        </div>
    )
}

export default MainPage