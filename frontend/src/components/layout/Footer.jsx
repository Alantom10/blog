import { BsGithub, BsLinkedin, BsEnvelopeFill, BsInstagram, BsDiscord } from "react-icons/bs";


function Footer() {
    return (
        <footer className="max-w-[1600px] mx-auto w-full bg-react-blue flex flex-col px-10 pt-10 h-[40vh] justify-between">
            <div className="flex flex-col md:flex-row justify-between">
                <div className="flex flex-col self-center md:self-start items-center md:items-start">
                    <h2 className="text-3xl lg:text-5xl font-semibold pb-10">Let's Connect !</h2>
                    <div className="flex gap-2 md:transition-transform md:duration-300 justify-between md:justify-start">
                        <a href="https://github.com/alantom10" target="_blank" rel="noopener noreferrer" className="border rounded-full w-10 h-10 flex justify-center items-center transition-colors duration-700 transform text-white shadow-md shadow-slate-950 hover:bg-white hover:text-react-blue hover:border-transparent">
                            <BsGithub className="text-xl" />
                        </a>
                        <a href="https://www.linkedin.com/in/alanthomas2000/" target="_blank" rel="noopener noreferrer" className="border rounded-full w-10 h-10 flex justify-center items-center transition-colors duration-700 transform text-white shadow-md shadow-slate-950 hover:bg-white hover:text-react-blue hover:border-transparent">
                            <BsLinkedin className="text-xl" />                        
                        </a>
                        <a href="mailto:acthomas2000@gmail.com" target="_blank" rel="noopener noreferrer" className="border rounded-full w-10 h-10 flex justify-center items-center transition-colors duration-700 transform text-white shadow-md shadow-slate-950 hover:bg-white hover:text-react-blue hover:border-transparent">
                            <BsEnvelopeFill className="text-xl" />                       
                        </a>
                        <a href="https://www.instagram.com/alan._.ct/" target="_blank" rel="noopener noreferrer" className="border rounded-full w-10 h-10 flex justify-center items-center transition-colors duration-700 transform text-white shadow-md shadow-slate-950 hover:bg-white hover:text-react-blue hover:border-transparent">
                            <BsInstagram className="text-xl" />                        
                        </a>
                        <a href="https://www.discordapp.com/users/443338198199042049" target="_blank" rel="noopener noreferrer" className="border rounded-full w-10 h-10 flex justify-center items-center transition-colors duration-700 transform text-white shadow-md shadow-slate-950 hover:bg-white hover:text-react-blue hover:border-transparent">
                            <BsDiscord className="text-xl" />                       
                        </a>
                    </div>
                </div>
                <div className="flex flex-col w-4/5 md:w-[450px] self-center pt-20 md:pt-0">
                    <h3 className="text-l lg:text-2xl self-center">Subscribe to my newsletter</h3>
                    <div className="relative mt-4">
                        <input type="email" id="newsletter-email" name="newsletter-email" placeholder="example@example.com" className="w-full h-12 rounded-full p-4 text-black shadow-custom "/>
                        <button className="w-28 h-10 rounded-full text-white bg-react-blue absolute right-1 top-1 shadow shadow-slate-950 transition-colors duration-700 transform hover:bg-white hover:text-react-blue hover:border-transparent">Subscribe</button>
                    </div>
                </div>
            </div>
            <p className="text-white text-sm pb-10 self-center pt-20 md:pt-6">© 2024 All Rights Reserved Alan Thomas</p>
        </footer>  
    );
};

export default Footer;