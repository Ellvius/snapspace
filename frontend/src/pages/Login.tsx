import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import type { FormEvent } from "react";


const Login = () => {
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const navigate = useNavigate();
    const { login } = useAuth();

    const handleLogin = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        login();
        navigate('/dashboard');
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-8">
                <h1 className="text-2xl font-semibold mb-6 text-center">Login</h1>
                <form onSubmit={handleLogin} className="space-y-4">
                    <div>
                        <label htmlFor="username" className="sr-only">
                            Username
                        </label>
                        <input 
                            type="text" 
                            id="username"
                            placeholder="Username"
                            className="block w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 focus:ring-indigo-500 focus:border-indigo-500"
                            value={username}    
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label htmlFor="password" className="sr-only">
                            Password
                        </label>
                        <input 
                            type="password" 
                            id="password"
                            placeholder="Password"
                            className="block w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 focus:ring-indigo-500 focus:border-indigo-500"
                            value={password}    
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button 
                        type="submit"
                        className="mt-8 w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition"
                    >
                        Login
                    </button>
                </form>
                <p 
                    onClick={() => navigate('/register')}
                    className="mt-2 text-center font-medium px-4 py-2 hover:text-indigo-600 cursor-pointer transition-colors"
                >
                    Don&apos;t have an account?{' '}
                    <span className="font-semibold hover:text-gray-800">Register</span>
                </p>
            </div>
        </div>
    );
}

export default Login;