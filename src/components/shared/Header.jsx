import Logo from "../../assets/alan.png";
import { Link } from "react-router-dom";

function Header() {
    return (
        <nav className="mx-auto flex items-center justify-between w-full lg:py-5 py-4 px-10 bg-transparent h-10vh fixed top-2 z-20">
            <div>
                <Link to="/">
                    <img src={Logo} alt="Alan Thomas Logo" className="h-24" />
                </Link>
            </div>

            <div className="flex justify-center items-center border border-white/[0.1] rounded-full w-28 h-9 shadow-md shadow-slate-950 text-sm text-center transition-colors duration-700 transform hover:bg-white hover:text-react-blue hover:border-transparent">
                <Link to="/about">
                    ABOUT
                </Link> 
            </div>
        </nav>      
    );
};

export default Header;