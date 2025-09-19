import Logo from "../../assets/alan.png";
import { Link } from "react-router-dom";

function Header() {
    return (
        // <header className="w-full bg-react-blue h-10vh fixed z-20 shadow border-b-[1px] border-solid border-white backdrop-blur-lg">
        <header className="max-w-[1600px] mx-auto flex items-center justify-between w-full lg:py-5 py-4 px-10 bg-transparent h-10vh fixed left-0 right-0 z-20">
            <div>
                <Link to="/">
                    <img src={ Logo } alt="Alan Thomas Logo" className="h-24" />
                </Link>
            </div>

            <nav className="flex justify-between items-center gap-4">
                <Link to="/about" className="inline-flex items-center justify-center border border-white/[0.1] bg-react-blue rounded-full px-4 h-10 shadow-md shadow-slate-950 text-sm text-white transition-colors duration-700 transform hover:bg-white hover:text-react-blue hover:border-transparent">
                    ABOUT
                </Link>
            </nav>
        </header>      
    );
};

export default Header;