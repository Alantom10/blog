function BlogPage() {
    return (
        <>
            <style>
                {`
                    p {
                        line-height: 2;
                        font-size: 1.2em;
                    }
                `}
            </style>
            <div className="max-w-[1200px] mx-auto w-full pb-10 md:pb-20 pt-20 px-10 box-content">
                <h1 className="text-3xl lg:text-5xl font-semibold py-20 md:pt-40">Understanding React Hooks</h1>
            </div>
        </>
    )
}

export default BlogPage;