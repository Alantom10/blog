import { useEffect } from 'react';
import authorProfileImage from "../assets/alan-profile.JPG"
import coverImage from "../assets/wd.jpg"
import CompSci from "../assets/compsci.png"

function BlogPage() {
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);
    
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
                <h1 className="text-3xl lg:text-5xl font-semibold py-10 md:pt-40 text-center">Understanding React Hooks</h1>

                <div className="flex font-light items-center justify-center">
                    <img src={authorProfileImage} alt="`Alan Thomas' profile`" className="rounded-full w-12 h-12 mr-2" />
                    <h4 className="px-2 text-xl">Alan Thomas</h4>
                    <div className="text-slate-500 px-2">•</div>
                    <p className="text-slate-500 px-2 font-light">August 9, 2024</p>
                </div>

                <img src={coverImage} alt="React Hooks Cover" className="w-full rounded-md mt-20 mb-10" />

                <p className="leading-7 text-lg mb-6">
                    React Hooks were introduced in React 16.8 and have since revolutionized how developers write functional components. Hooks allow you to use state and other React features without writing a class. In this blog, we will dive deep into the most commonly used hooks and how they can simplify your React development.
                </p>

                <h2 className="text-2xl font-semibold mb-4">What are React Hooks?</h2>
                <p className="leading-7 text-lg mb-6">
                    React Hooks are functions that let you use state and lifecycle features in functional components. Before hooks, these features were only available in class components. Hooks have made functional components more powerful, and it's now possible to build complex applications using only functions.
                </p>

                <h2 className="text-2xl font-semibold mb-4">useState Hook</h2>
                <p className="leading-7 text-lg mb-6">
                    The <code className="rounded px-2 py-0.5">useState</code> hook allows you to add state to your functional components. It's similar to this.state in class components. Here's an example:
                </p>

                <div className="code rounded-lg">
                    <pre className="text-white p-4 rounded-lg mb-6">
                        <code>
                            {`import React, { useState } from 'react';

                            function Counter() {
                                const [count, setCount] = useState(0);

                                return (
                                    <div>
                                        <p>You clicked {count} times</p>
                                        <button onClick={() => setCount(count + 1)}>
                                            Click me
                                        </button>
                                    </div>
                                );
                            }`}
                        </code>
                    </pre>
                </div>

                <p className="leading-7 text-lg mb-6">
                    In this example, the <code className="rounded px-2 py-0.5">useState</code> hook initializes the <code className="rounded px-2 py-0.5">count</code> variable to 0. The <code className="rounded px-2 py-0.5">setCount</code> function is used to update the count value, and the component re-renders whenever the state changes.
                </p>

                <h2 className="text-2xl font-semibold mb-4">useEffect Hook</h2>
                <p className="leading-7 text-lg mb-6">
                    The <code className="rounded px-2 py-0.5">useEffect</code> hook allows you to perform side effects in your components. It's similar to lifecycle methods like componentDidMount, componentDidUpdate, and componentWillUnmount in class components. Here's an example:
                </p>

                <div className="code rounded-lg">
                    <pre className="text-white p-4 mb-6">
                        <code>
                            {`import React, { useState, useEffect } from 'react';

                            function Example() {
                                const [count, setCount] = useState(0);

                                useEffect(() => {
                                    document.title = \`You clicked \${count} times\`;
                                }, [count]);

                                return (
                                    <div>
                                        <p>You clicked {count} times</p>
                                        <button onClick={() => setCount(count + 1)}>
                                            Click me
                                        </button>
                                    </div>
                                );
                            }`}
                        </code>
                    </pre>
                </div>

                <p className="leading-7 text-lg mb-6">
                    In this example, the <code className="rounded px-2 py-0.5">useEffect</code> hook updates the document title whenever the <code className="rounded px-2 py-0.5">count</code> changes. The second argument to <code className="rounded px-2 py-0.5">useEffect</code> is an array of dependencies, ensuring the effect only runs when the <code className="rounded px-2 py-0.5">count</code> value changes.
                </p>

                <h2 className="text-2xl font-semibold mb-4">Conclusion</h2>
                <p className="leading-7 text-lg mb-6">
                    React Hooks have fundamentally changed how we write React components. They provide a cleaner and more concise way to use state and other React features in functional components. As you continue to work with Hooks, you'll discover how they simplify your code and improve your development workflow.
                </p>
            </div>
        </>
    )
}

export default BlogPage;