import { Link } from "react-router-dom";

function Card({ title, intro, coverImage, authorName, authorProfileImage, datePublished, layoutType }) {
    return (
        <>
            { layoutType === 'main' ? (
                <Link to="/blog-page" className="col-span-12 row-span-3">
                    <div className="flex rounded-md shadow-custom transition-shadow duration-700 transform hover:shadow-md hover:shadow-slate-950">
                        <div className="p-10 flex flex-col">
                            <h2 className="text-3xl lg:text-5xl font-semibold pb-8"> {title} </h2>
                            <p className="pt-5 pb-10"> {intro} </p>
                            <div className="flex mt-auto">
                                <img src={authorProfileImage} alt={`${authorName}'s profile`} className="rounded-full w-12 h-12" />
                                <div className="pl-5 font-light">
                                    <h4> {authorName} </h4>
                                    <p className="text-slate-500"> {datePublished} </p>
                                </div>
                            </div>
                        </div>
                        <img src={coverImage} alt={`${title} cover`} className="object-cover w-1/2 rounded-r-md" />
                    </div>
                </Link>
            ) : (
                <Link to="/blog-page" className=" col-span-6 row-span-4">
                    <div className="flex flex-col rounded-md shadow-custom transition-shadow duration-700 transform hover:shadow-md hover:shadow-slate-950">
                        <img src={coverImage} alt={`${title} cover`} className="object-cover rounded-t-md" />
                        <div className="p-7 flex flex-col">
                            <h2 className="text-3xl lg:text-4xl font-semibold pb-3"> {title} </h2>
                            <p className="pb-5"> {intro} </p>
                            <div className="flex">
                                <img src={authorProfileImage} alt={`${authorName}'s profile`} className="rounded-full w-12 h-12" />
                                <div className="pl-5 font-light">
                                    <h4> {authorName} </h4>
                                    <p className="text-slate-500"> {datePublished} </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </Link>
            ) }
        </>
    )
}

export default Card;