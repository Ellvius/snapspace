import { useAuth } from "../context/AuthContext";

const Dashboard = () => {
    const {logout} = useAuth();

    const logoutUser = ()=> {
        logout();
    }
    return (
        <div>
            <button onClick={logoutUser}>Logout</button>
        </div>
    );
}

export default Dashboard;