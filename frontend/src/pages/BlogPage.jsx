import parse from 'html-react-parser';
import { useEffect, useState } from "react";
import { getBlogBySlug } from "../api/blogsApi";

import authorProfileImage from "../assets/alan-profile.JPG";
import blogCoverImage from "../assets/wd.jpg";
import { useParams } from 'react-router-dom';
import { Helix } from 'ldrs/react';
import 'ldrs/react/Helix.css';


function BlogPage() {
    const [loading, setLoading] = useState(true);
    const { slug } = useParams();
    const [blog, setBlog] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const data = await getBlogBySlug(slug);
                setBlog(data);
                setLoading(false);
            } catch (err) {
                setError(err.message);
            }
        }
        fetchData();
        window.scrollTo(0, 0);
    }, [slug]);

    if (error) return <p className="w-full h-[60vh] content-center text-center">Error: {error}</p>;

    if (loading) {
        return (
            <div className="w-full h-[60vh] content-center text-center">
                <Helix
                    size="150"
                    speed="2.5"
                    color="white" 
                />
            </div>
        );
    }

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
                <h1 className="text-3xl lg:text-5xl font-semibold py-10 md:pt-40 text-center">{ blog.title }</h1>

                <div className="flex font-light items-center justify-center">
                    <img src={ authorProfileImage } alt={`${blog.author.name}' profile`} className="rounded-full w-12 h-12 mr-2" />
                    <h4 className="px-2 text-xl">{ blog.author.name }</h4>
                    <div className="text-slate-500 px-2">•</div>
                    <p className="text-slate-500 px-2 font-light">{ blog.datePublished }</p>
                </div>

                <img src={ blogCoverImage } alt={`${blog.title} cover`} className="w-full rounded-md mt-20 mb-10" />
                
                { parse(blog.content) }

            </div>
        </>
    )
}

export default BlogPage;