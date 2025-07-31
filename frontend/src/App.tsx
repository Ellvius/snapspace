import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

const App = () => {
    const { isLoggedIn } = useAuth();

    return (
        <Routes>
            <Route path='/' element={isLoggedIn ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
            <Route path='/login' element={!isLoggedIn ? <Login/> : <Navigate to="/dashboard"/>}/>
            <Route path='/register' element={!isLoggedIn ? <Register/> : <Navigate to="/dashboard"/>} />
            <Route
                path="/dashboard"
                element={isLoggedIn ? <Dashboard /> : <Navigate to="/login" />}
            />
        </Routes>
    )
}

export default App;
