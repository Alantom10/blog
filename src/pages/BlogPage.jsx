import { useEffect } from 'react';
import Data from "../data/mock.json"

import authorProfileImage from "../assets/alan-profile.JPG"
import coverImage from "../assets/wd.jpg"
import CompSci from "../assets/compsci.png"

function BlogPage() {
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    const blogData = Data;
    // const profileImage = require(`../assets/${blogData.author.profileImage}`);
    // const coverImage = require(`../assets/${blogData.coverImage}`);

    const renderParagraph = (text, highlights) => {
        if (!highlights.length) return <p className="leading-7 text-lg mb-6">{ text }</p>;

        const parts = text.split(new RegExp(`(${highlights.join('|')})`, 'g'));

        return (
            <p className="leading-7 text-lg mb-6">
                {parts.map((part, i) =>
                    highlights.includes(part) ? (
                        <code key={i} className="rounded px-2 py-0.5">{ part }</code>
                    ) : (
                        part
                    )
                )}
            </p>
        )
    }

    const renderContent = (content) => {
        return content.map((block, index) => {
            switch (block.type) {
                case 'heading':
                    const HeadingTag = `h${block.level}`;
                    return <HeadingTag key={index} className="text-2xl font-semibold mb-4">{ block.text }</HeadingTag>
                case 'paragraph':
                    return <div key={index}>{ renderParagraph(block.text, block.highlights) }</div>
                case 'code':
                    return (
                        <div className="code rounded-lg">
                            <pre key={index} className="text-white p-4 rounded-lg mb-6">
                                <code>{ block.code }</code>
                            </pre>
                        </div>
                    );
                // case 'image':
                //     return <img src={ require(`../assets/${block.url}`) } alt="Example" className="w-full rounded-md mt-10 mb-6" />
                case 'image':
                    return <img src={ CompSci } alt="Example" className="w-full rounded-md mt-10 mb-6"/>
                default:
                    return null;
            }
        });
    };
    
    return (
        <>
            <style>
                {`
                    p {
                        line-height: 2;
                        font-size: 1.2em;
                        font-weight: 200;
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

                <img src={ coverImage } alt={`${blogData.title} cover`} className="w-full rounded-md mt-20 mb-10" />
                
                { renderContent(blogData.content) }

            </div>
        </>
    )
}

export default BlogPage;