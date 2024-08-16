import { useEffect } from 'react';
import parse from 'html-react-parser';
import Data from "../data/mock.json"

import authorProfileImage from "../assets/alan-profile.JPG"

function BlogPage() {
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    const blogData = Data[0];
    // const profileImage = require(`../assets/${blogData.author.profileImage}`);
    // const coverImage = require(`../assets/${blogData.coverImage}`);

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
            <div className="max-w-[960px] mx-auto w-full pb-10 md:pb-20 pt-20 px-10 box-content">
                <h1 className="text-3xl lg:text-5xl font-semibold py-10 md:pt-40 text-center">{ blogData.title }</h1>

                <div className="flex font-light items-center justify-center">
                    <img src={ authorProfileImage } alt="`Alan Thomas' profile`" className="rounded-full w-12 h-12 mr-2" />
                    <h4 className="px-2 text-xl">{ blogData.author.name }</h4>
                    <div className="text-slate-500 px-2">•</div>
                    <p className="text-slate-500 px-2 font-light">{ blogData.datePublished }</p>
                </div>

                <img src={ blogData.coverImage } alt={`${blogData.title} cover`} className="w-full rounded-md mt-20 mb-10" />
                
                { parse(blogData.content) }

            </div>
        </>
    )
}

export default BlogPage;