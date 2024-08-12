import Card from "../components/Card";
import authorProfileImage from "../assets/alan-profile.JPG"
import coverImage from "../assets/wd.jpg"

function Home() {
    return (
        <div className="max-w-[960px] mx-auto w-full pb-10 md:pb-20 pt-20 px-10 box-content">
            <div className="grid grid-cols-12 grid-rows-layout gap-[50px] py-20 md:pt-40">
                <Card
                    title="Understanding React Hooks"
                    intro="React Hooks are a powerful addition to the React API that allows developers to use state and other features in functional components..."
                    coverImage={ coverImage }
                    authorName="Alan Thomas"
                    authorProfileImage={ authorProfileImage }
                    datePublished="August 9, 2024"
                    layoutType="main"
                />

                <Card
                    title="Understanding React Hooks"
                    intro="React Hooks are a powerful addition to the React API that allows developers to use state and other features in functional components..."
                    coverImage={ coverImage }
                    authorName="Alan Thomas"
                    authorProfileImage={ authorProfileImage }
                    datePublished="August 9, 2024"
                />

                <Card
                    title="Understanding React Hooks"
                    intro="React Hooks are a powerful addition to the React API that allows developers to use state and other features in functional components..."
                    coverImage={ coverImage }
                    authorName="Alan Thomas"
                    authorProfileImage={ authorProfileImage }
                    datePublished="August 9, 2024"
                />
            </div>
        </div>

    )
};

export default Home;