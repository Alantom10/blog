import parse from 'html-react-parser';

import authorProfileImage from "../assets/alan-profile.JPG"

function PreviewPost({ title, author, coverImage, datePublished, content, onClose }) {
    return (
        <>
            <style>
                {`
                    p {
                        line-height: 2;
                        font-size: 1.2em;
                        font-weight: 200;
                    }

                    h2 {
                        font-size: 1.5rem;
                        line-height: 2rem;
                        font-weight: 600;
                    }

                    h3 {
                        font-size: 1.25rem;
                        line-height: 1.75rem;
                        font-weight: 600;
                    }

                    pre {
                        background-color: var(--code-background);
                        font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
                            monospace;
                        padding: 1rem;
                        border-radius: 0.5rem;
                    }

                    img {
                        border-radius: 0.5rem;
                    }
                `}
            </style>
            <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-md flex justify-center items-center z-50 overflow-y-auto">
                <div className="bg-react-blue pb-10 md:pb-20 px-10 max-w-[960px] mx-auto w-full relative overflow-y-auto max-h-full">
                    <button 
                        className="fixed top-14 right-14 flex justify-center items-center border border-white/[0.1] bg-react-blue rounded-full w-9 h-9 shadow-md shadow-slate-950 text-sm text-center transition-colors duration-700 transform hover:bg-white hover:text-react-blue hover:border-transparent" 
                        onClick={onClose}>
                            X
                    </button>
                    <h1 className="text-3xl lg:text-5xl font-semibold pb-10 pt-20 text-center">{ title }</h1>

                    <div className="flex font-light items-center justify-center">
                        <img src={ authorProfileImage } alt={`${author.name}' profile`} className="rounded-full w-12 h-12 mr-2" />
                        <h4 className="px-2 text-xl">{ author.name }</h4>
                        <div className="text-slate-500 px-2">•</div>
                        <p className="text-slate-500 px-2 font-light">{ datePublished }</p>
                    </div>

                    <img src={ coverImage } alt={`${title} cover`} className="w-full rounded-md mt-20 mb-10" />
                    
                    { parse(content) }

                </div>
            </div>
        </>
    )
}

export default PreviewPost;