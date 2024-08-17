import Card from "../components/Card";
import Data from "../data/mock.json"
import authorProfileImage from "../assets/alan-profile.JPG"

function Home() {
    function formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', options);
    }

    function stripHtml(html) {
        let div = document.createElement("div");
        div.innerHTML = html;
        return div.textContent || div.innerText || "";
    }
    
    function generateIntro(content, wordLimit) {
        const text = stripHtml(content);
        const words = text.split(' ');
        return words.slice(0, wordLimit).join(' ') + (words.length > wordLimit ? '...' : '');
    }    

    return (
        <div className="max-w-[960px] mx-auto w-full pb-10 md:pb-20 pt-20 px-10 box-content">
            <div className="grid grid-cols-12 grid-rows-layout gap-[50px] py-20 md:pt-40">
            {Data.map((blog, index) => (
                    <Card
                        key={index}
                        title={blog.title}
                        intro={generateIntro(blog.content, 20)}
                        coverImage={blog.coverImage}  // Use blog.coverImage if coverImage URLs are in JSON
                        authorName={blog.author.name}
                        authorProfileImage={authorProfileImage}  // Use blog.authorProfileImage if URLs are in JSON
                        datePublished={formatDate(blog.datePublished)}
                        layoutType={index % 3 === 0 ? 'main' : 'normal'}
                    />
                ))}
            </div>
        </div>
    )
};

export default Home;