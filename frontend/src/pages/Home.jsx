import Card from "../components/ui/Card";
import authorProfileImage from "../assets/alan-profile.JPG";
import blogCoverImage from "../assets/wd.jpg";
import { useEffect, useState } from "react";
import { getBlogs } from "../api/blogsApi";
import Spinner from "../components/ui/Spinner";

function Home() {
  const [loading, setLoading] = useState(true);
  const [blogs, setBlogs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getBlogs();
        setBlogs(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
      }
    }
    fetchData();
  }, []);

  if (error)
    return (
      <p className="w-full h-[60vh] content-center text-center">
        Error: {error}
      </p>
    );

  function formatDate(dateString) {
    const options = { year: "numeric", month: "long", day: "numeric" };
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", options);
  }

  function stripHtml(html) {
    let div = document.createElement("div");
    div.innerHTML = html;
    return div.textContent || div.innerText || "";
  }

  function generateIntro(content, wordLimit) {
    const text = stripHtml(content);
    const words = text.split(" ");
    return (
      words.slice(0, wordLimit).join(" ") +
      (words.length > wordLimit ? "..." : "")
    );
  }

  return (
    <>
      {loading ? (
        <Spinner />
      ) : (
        <div className="max-w-[960px] mx-auto w-full pb-10 md:pb-20 pt-20 px-10 box-content">
          <div className="grid grid-cols-12 auto-rows-[100px] gap-[50px] py-20 md:pt-40">
            {blogs.map((blog, index) => (
              <Card
                key={blog.slug}
                slug={blog.slug}
                title={blog.title}
                intro={generateIntro(blog.content, 20)}
                // coverImage={blog.coverImage}  // Use blog.coverImage if coverImage URLs are in JSON
                coverImage={blogCoverImage}
                authorName={blog.author.name}
                authorProfileImage={authorProfileImage} // Use blog.authorProfileImage if URLs are in JSON
                datePublished={formatDate(blog.date_published)}
                layoutType={index % 3 === 0 ? "main" : "normal"}
              />
            ))}
          </div>
        </div>
      )}
    </>
  );
}

export default Home;
