import Card from "../components/Card";
import authorProfileImage from "../assets/alan-profile.JPG"
import coverImage from "../assets/wd.jpg"

function Home() {
    return (
        <div className="md:max-w-[1200px] lg:max-w-[1400px] mx-auto w-full pb-10 md:pb-20 pt-20 px-10">
            <div className="grid grid-cols-2 grid-rows-2 gap-8 py-20 md:pt-40">
                <Card
                    title="Understanding React Hooks"
                    intro="React Hooks are a powerful addition to the React API that allows developers to use state and other features in functional components..."
                    coverImage={ coverImage }
                    authorName="Alan Thomas"
                    authorProfileImage={ authorProfileImage }
                    datePublished="August 9, 2024"
                />
            </div>
            {/* <h1 className="py-20 md:pt-40 ">Welcome to the Home Page</h1>
            <p>This is the home page content.</p> */}
        </div>

    )
};

export default Home;