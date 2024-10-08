import Logo from "../../assets/alan.png";
import { Link } from "react-router-dom";

function Header() {
    return (
        // <header className="w-full bg-[#1F2329]/[0.5] h-10vh fixed z-20 shadow-md shadow-slate-950 backdrop-blur-lg">
        <nav className="max-w-[1600px] mx-auto flex items-center justify-between w-full lg:py-5 py-4 px-10 bg-transparent h-10vh fixed left-0 right-0 z-20">
            <div>
                <Link to="/">
                    <img src={ Logo } alt="Alan Thomas Logo" className="h-24" />
                </Link>
            </div>

            <div className="flex justify-center items-center border border-white/[0.1] bg-react-blue rounded-full w-28 h-9 shadow-md shadow-slate-950 text-sm text-center transition-colors duration-700 transform hover:bg-white hover:text-react-blue hover:border-transparent">
                <Link to="/about">
                    ABOUT
                </Link> 
            </div>
        </nav>      
    );
};

export default Header;