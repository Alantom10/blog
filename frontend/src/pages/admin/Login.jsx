import { useState } from "react";
import Logo from "../../assets/alan.png";
import { BsPerson, BsLock, BsEye, BsEyeSlash, BsBoxArrowInRight } from "react-icons/bs";
import { useNavigate } from "react-router-dom";
import { login } from '../../api/authApi'; 


function Login() {
    const [showPassword, setShowPassword] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [errors, setErrors] = useState({});
    const [credentials, setCredentials] = useState({
        username: '',
        password: ''
    });

    const navigate = useNavigate();

    const handleChange = (e) => {
        setCredentials({
            ...credentials,
            [e.target.name]: e.target.value
        });
        // Clear errors when user starts typing
        if (errors.general) {
            setErrors({});
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setErrors({});

        try {
            // Basic validation
            if (!credentials.username.trim()) {
                setErrors({ username: 'Username is required' });
                setIsLoading(false);
                return;
            }
            if (!credentials.password.trim()) {
                setErrors({ password: 'Password is required' });
                setIsLoading(false);
                return;
            }

            const response = await login(credentials);
        
            localStorage.setItem('token', response.access_token);
            
           navigate('/dashboard');
            
        } catch (error) {
            setErrors({ general: error.message || 'Login failed' });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            <div className="max-w-[960px] mx-auto w-full px-10 box-content">
                <div className="flex flex-col py-20">
                    
                    <div className="text-center mb-10">
                        <div className="mx-auto w-20 h-20 bg-gradient-to-r from-blue-500 to-cyan-400 rounded-lg flex items-center justify-center mb-4">
                            <img src={ Logo } alt="Alan Thomas Logo" className="h-20" />
                        </div>
                        <h2 className="text-3xl font-bold text-white mb-2">Admin Login</h2>
                    </div>

                    <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl shadow-2xl p-8 border border-gray-700/50 min-w-96 mx-auto w-3/5">
                        {errors.general && (
                            <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
                                {errors.general}
                            </div>
                        )}
                        <form onSubmit={handleSubmit} className="space-y-6">

                            <div>
                                <label htmlFor="username" className="block text-sm font-medium text-gray-300 mb-2">
                                    Username
                                </label>
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                        <BsPerson className="text-lg text-gray-400" />
                                    </div>
                                    <input 
                                        id="username"
                                        name="username"
                                        type="text" 
                                        value={credentials.username}
                                        onChange={handleChange}
                                        placeholder="Enter your username"
                                        className="w-full block pl-10 pr-3 py-3 border rounded-lg bg-gray-700/50 text-white placeholder-gray-400 focus:outline-none focus:ring-2 transition-colors border-gray-600 focus:ring-blue-500/20 focus:border-blue-400"/>
                                </div>
                            </div>

                            <div>
                                <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                                    Password
                                </label>
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                        <BsLock className="text-lg text-gray-400" />
                                    </div>
                                    <input 
                                        id="password"
                                        name="password"
                                        type={showPassword ? 'text' : 'password'} 
                                        value={credentials.password}
                                        onChange={handleChange}
                                        placeholder="Enter your password"
                                        className="w-full block pl-10 pr-3 py-3 border rounded-lg bg-gray-700/50 text-white placeholder-gray-400 focus:outline-none focus:ring-2 transition-colors border-gray-600 focus:ring-blue-500/20 focus:border-blue-400"/>
                                    <button 
                                        type="button"
                                        className="absolute inset-y-0 right-0 pr-3 flex items-center"
                                        onClick={() => setShowPassword(!showPassword)}
                                    >
                                        {showPassword ? (
                                            <BsEye className="text-lg text-gray-400 hover:text-gray-300" />
                                        ) : (
                                            <BsEyeSlash className="text-lg text-gray-400 hover:text-gray-300" />
                                        )}
                                    </button>
                                </div>
                            </div>

                            <div className="flex items-center justify-between">
                                <div className="flex items-center">
                                    <input 
                                        id="remember-me"
                                        name="remember-me"
                                        type="checkbox" 
                                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-600 bg-gray-700 rounded"    
                                    />
                                    <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-300">
                                        Remember me
                                    </label>
                                </div>
                                <div className="text-sm">
                                    <a href="#" className="font-medium text-blue-400 hover:text-blue-300 transition-colors">
                                        Forgot password
                                    </a>
                                </div>
                            </div>

                            <button
                                disabled={isLoading}
                                type="submit"
                                className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                                >
                                {isLoading ? (
                                    <div className="flex items-center">
                                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        Signing in...
                                    </div>
                                ) : (
                                    <div className="flex items-center">
                                        <BsBoxArrowInRight className="text-lg mr-2" />
                                        Sign in
                                    </div>
                                )}
                            </button>

                        </form>

                        <div className="mt-6 text-center">
                            <a href="/" className="text-sm text-gray-400 hover:text-gray-300 transition-colors">
                                ← Back to blog
                            </a>
                        </div>
                    </div>

                </div>
            </div>
        </>
    )
};

export default Login;