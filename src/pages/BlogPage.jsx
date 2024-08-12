import authorProfileImage from "../assets/alan-profile.JPG"
import coverImage from "../assets/wd.jpg"
import CompSci from "../assets/compsci.png"

function BlogPage() {
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

                <div className="prose max-w-none px-10">
                    <h2 className="text-2xl lg:text-3xl font-semibold mt-12">Introduction to React Hooks</h2>
                    <p className="mt-6">React Hooks are functions that let you use state and other React features without writing a class...</p>
                    
                    <h3 className="text-xl lg:text-2xl font-semibold mt-10">Understanding useState</h3>
                    <p className="mt-4">The `useState` hook allows you to add state to functional components...</p>

                    <div className="bg-gray-800 text-white rounded-md p-6 mt-6">
                        <pre>
                            <code>
                                {`const [count, setCount] = useState(0);`}
                            </code>
                        </pre>
                    </div>

                    <img src={ CompSci } alt="Example" className="w-full rounded-md mt-10 mb-6" />
                </div>
            </div>
        </>
    )
}

export default BlogPage;