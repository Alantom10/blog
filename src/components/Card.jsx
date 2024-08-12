function Card({ title, intro, coverImage, authorName, authorProfileImage, datePublished }) {
    return (
        <div className="flex rounded-md col-span-2 min-h-[500px] shadow-custom transition-shadow duration-700 transform hover:shadow-md hover:shadow-slate-950">
            <div className="p-10 relative">
                <h2 className="text-3xl lg:text-5xl font-semibold pb-8"> { title } </h2>
                <p className="pt-5 pb-10"> { intro } </p>
                <div className="flex absolute bottom-10">
                    <img src={ authorProfileImage } alt={`${ authorName }'s profile`} className="rounded-full w-12 h-12" />
                    <div className="pl-5 font-light">
                        <h4> { authorName } </h4>
                        <p className="text-slate-500"> { datePublished } </p>
                    </div>
                </div>
            </div>
            <img src={ coverImage } alt={`${ title } cover`} className="object-cover w-1/2 rounded-r-md" />
        </div>
    )
}

export default Card;