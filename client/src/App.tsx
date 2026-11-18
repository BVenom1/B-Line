import "./App.css";
import MainPage from "./components/main page/MainPage";
import AlertHandler from "./components/alerts/AlertHandler";
import { ReactNode, useState } from "react";
import { GroupModel } from "./components/interfaces";
import GroupPage from "./components/group page/GroupPage";
import ErrorPage from "./components/misc/ErrorPage";

function App() {
    enum DisplayedPage {
        main = 'MAIN',
        group = 'GROUP'
    }
    const [page, setPage] = useState<DisplayedPage>(DisplayedPage.main);
    const [group, setGroup] = useState<GroupModel | null>(null);

    const onGroupButtonClick = (g: GroupModel) => {
        setGroup(g);
        setPage(DisplayedPage.group);
    }

    const pageMap: Record<DisplayedPage, ReactNode> = {
        [DisplayedPage.main]: <MainPage onGroupButtonClick={onGroupButtonClick} />,
        [DisplayedPage.group]: group
            ? <GroupPage group={group} onReturnButtonClick={() => setPage(DisplayedPage.main)} />
            : <ErrorPage onReturnButtonClick={() => setPage(DisplayedPage.main)}>
                <div className="column">
                    <h1 className="no-margin left-align alert-heading-Error">Error:</h1>
                    <p className="no-margin left-align">Could not load group</p>
                </div>
            </ErrorPage>
    }

    return (
        <div>
            {pageMap[page]}
            <AlertHandler />
        </div>
    )

}

export default App;
