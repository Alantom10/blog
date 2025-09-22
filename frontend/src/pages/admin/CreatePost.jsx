import { useEffect, useState } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import 'quill/dist/quill.snow.css';
import ReactQuill from 'react-quill';
import { getBlogBySlug, createBlog, updateBlog } from '../../api/blogsApi'; 
import PreviewPost from '../../components/ui/PreviewPost';
import Spinner from "../../components/ui/Spinner";
import { useNavigate } from 'react-router-dom';
import {
    BsEye,
    BsTrash,
} from "react-icons/bs";
import { RiDraftLine } from "react-icons/ri";


function CreatePost() {
    const [title, setTitle] = useState('');
    const [slug, setSlug] = useState("");
    const [coverImage, setCoverImage] = useState('');
    const [coverImageName, setCoverImageName] = useState('');
    const [tags, setTags] = useState([]);
    const [tagInput, setTagInput] = useState('');
    const [content, setContent] = useState('');
    const [showPreview, setShowPreview] = useState(false);
    const [isEditMode, setIsEditMode] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [originalBlog, setOriginalBlog] = useState(null);

    const { slug: blogSlug } = useParams(); // Get slug from URL params
    const location = useLocation();
    const navigate = useNavigate();


    useEffect(() => {
        window.scrollTo(0, 0);

        if (blogSlug) {
            setIsEditMode(true);
            fetchBlogData(blogSlug);
        }
    }, [blogSlug]);

    const fetchBlogData = async (slug) => {
        setLoading(true);
        setError(null);

        try {
            const blog = await getBlogBySlug(slug);
            if (blog) {
                setOriginalBlog(blog);
                setTitle(blog.title);
                setSlug(blog.slug);
                setContent(blog.content);
                setCoverImage(blog.cover_image);
                setTags(blog.tags || []);

                if (blog.cover_image) {
                    setCoverImageName('Existing image')
                }
            }
        } catch (err) {
            setError(err.message);
            console.error('Error fetching blog:', err);
        } finally {
            setLoading(false);
        }
    }

    const handleProcedureContentChange = (content) => {
        setContent(content);
    };

    const handleTitleChange = (e) => {
        const newTitle = e.target.value;
        setTitle(newTitle);

        if (!isEditMode) {
            var slugify = require('slug');
            setSlug(slugify(newTitle));
        }
    };

    const handleCoverImageChange = (e) => {
        const file = e.target.files[0];

        if (file) {
            setCoverImageName(file.name); // Update file name
            const reader = new FileReader();
            reader.onloadend = () => {
                const base64String = reader.result;
                setCoverImage(base64String);
            };
            reader.readAsDataURL(file);
        } else {
            setCoverImageName(''); // Clear file name if no file is selected
        }
    };

    const togglePreview = () => {
        setShowPreview(!showPreview);
        if (!showPreview) {
            document.body.classList.add('no-scroll');
        } else {
            document.body.classList.remove('no-scroll');
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault()
            if (tagInput.trim() !== '') {
                setTags([...tags, tagInput.trim()]);
                setTagInput('');
            }
        }
    }

    const saveDraft = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const postData = {
                title: title.trim(),
                slug: slug.trim(),
                author: {
                    name: "Alan Thomas",
                    image: "alan-profile.JPG",
                },
                cover_image: coverImage || '',
                // datePublished: new Date().toLocaleDateString(),
                content: content,
                tags: tags,
                is_published: false
            };

            if (isEditMode) {
                // Update existing post using original slug
                await updateBlog(originalBlog.slug, postData);
                alert('Blog draft updated successfully!');
            } else {
                // Create new post - MongoDB will auto-generate ID
                await createBlog(postData);
                alert('Blog saved to draft successfully!');
            }

        } catch (error) {
            console.error("Error saving post:", error);
            alert(`Failed to add blog to draft. Please try again.`);
        } finally {
            setLoading(false);
        }
    }

    const savePost = async (e) => {
        e.preventDefault();

        // Basic validation
        if (!title.trim()) {
            alert('Title is required');
            return;
        }
        if (!content.trim()) {
            alert('Content is required');
            return;
        }
        if (!slug.trim()) {
            alert('Slug is required');
            return;
        }

        setLoading(true);

        try {
            const postData = {
                title: title.trim(),
                slug: slug.trim(),
                author_id: "68c6a027dc90b4465cb25046",
                author: {
                    name: "Alan Thomas",
                    image: "alan-profile.JPG",
                },
                cover_image: coverImage || '',
                datePublished: new Date().toISOString(),
                content: content,
                tags: tags,
                is_published: true
            };

            if (isEditMode) {
                // Update existing post using original slug
                await updateBlog(originalBlog.slug, postData);
                alert('Blog updated successfully!');
            } else {
                console.log('Sending data:', JSON.stringify(postData, null, 2));
                // Create new post - MongoDB will auto-generate ID
                await createBlog(postData);
                alert('Blog created successfully!');

                // Reset form after successful creation
                setTitle('');
                setSlug('');
                setContent('');
                setCoverImage('');
                setCoverImageName('');
                setTags([]);
                setTagInput('');
            }

        } catch (error) {
            console.error("Error saving post:", error);
            alert(`Failed to ${isEditMode ? 'update' : 'create'} blog. Please try again.`);
        } finally {
            setLoading(false);
        }
    }

    // Loading state while fetching blog data
    if (loading && isEditMode && !originalBlog) {
        return <Spinner />;
    }

    // Error state
    if (error) {
        return (
            <div className="max-w-[960px] mx-auto w-full pb-10 md:pb-20 box-content">
                <h1 className="text-center text-3xl lg:text-5xl font-semibold pt-10 pb-20">Error</h1>
                <p className="text-center text-red-500">Error loading blog: {error}</p>
            </div>
        );
    }

    var modules = {
        toolbar: [
            [{ 'header': [2, 3, false] }],
            // [{ 'font': [] }],
            // [{ size: ["small", false, "large", "huge"] }],
            ["bold", "italic", "underline", "strike", "blockquote"],
            [
                { list: "ordered" },
                { list: "bullet" },
                { indent: "-1" },
                { indent: "+1" },
                { align: [] }
            ],
            ["link", "image", 'video', "code-block"],
            [{ "color": ["#000000", "#e60000", "#ff9900", "#ffff00", "#008a00", "#0066cc", "#9933ff", "#ffffff", "#facccc", "#ffebcc", "#ffffcc", "#cce8cc", "#cce0f5", "#ebd6ff", "#bbbbbb", "#f06666", "#ffc266", "#ffff66", "#66b966", "#66a3e0", "#c285ff", "#888888", "#a10000", "#b26b00", "#b2b200", "#006100", "#0047b2", "#6b24b2", "#444444", "#5c0000", "#663d00", "#666600", "#003700", "#002966", "#3d1466", 'custom-color'] }],
            ['clean']
        ]
    };

    var formats = [
        "header",
        // "font", "height",
        "bold", "italic",
        "underline", "strike", "blockquote",
        "list", "color", "bullet", "indent",
        "link", "image", "video", "align", "size", "code-block",
    ];

    return (
        <>
            <style>
                {`
                    .ql-editor::before {
                        color: rgb(148 163 184) !important;
                        opacity: 1;
                    }

                    /* Change the color of all toolbar icons and text */
                    .ql-snow .ql-formats .ql-picker-label::before {
                        color: white;
                    }

                    /* Change the color of toolbar SVG icons */
                    .ql-toolbar .ql-formats button svg,
                    .ql-toolbar .ql-formats button .ql-fill {
                        fill: white;
                    }

                    .ql-snow .ql-stroke {
                        stroke: white;
                    }
                `}
            </style>
            <div className="max-w-[960px] mx-auto w-full pb-10 md:pb-20 box-content">
                <h1 className="text-center text-3xl lg:text-5xl font-semibold pt-10 pb-20">Create Post</h1>



                <div className="w-full mx-3">
                    <form onSubmit={savePost}>
                        <input
                            type="text"
                            className='bg-react-blue border p-2 mb-5 w-full'
                            value={title}
                            onChange={handleTitleChange}
                            placeholder="Blog Title"
                            required
                        />

                        <input
                            type="text"
                            className='bg-react-blue border p-2 mb-5 w-full'
                            value={slug}
                            placeholder="Blog Slug"
                        />

                        <div className='border p-2 mb-5 w-full relative flex'>
                            <label
                                for="upload-photo"
                                className='flex justify-center items-center border border-white bg-react-blue rounded-full w-32 h-9'>
                                Cover Image
                            </label>
                            <input
                                type="file"
                                name="photo"
                                id="upload-photo"
                                accept="image/*"
                                className='bg-react-blue opacity-0 absolute -z-10 left-10 top-1/2 transform -translate-y-1/2'
                                onChange={handleCoverImageChange}
                                placeholder="Upload Cover Image"
                            />
                            <span className='self-center ml-3'>{coverImageName ? `${coverImageName}` : 'No file selected'}</span>
                        </div>

                        <div className='flex flex-wrap gap-2 mb-5 w-full'>
                            {tags.map((tag, index) => (
                                <span
                                    key={index}
                                    className='inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold text-blue-300 bg-blue-500/20'    
                                >
                                    {tag}
                                    <button
                                        type='button'
                                        onClick={() => { 
                                            const newTags = tags.filter((_, i) => i !== index);
                                            setTags(newTags);
                                         }}
                                        className='ml-2 text-blue-300 hover:text-red-400'    
                                    >
                                        ×
                                    </button>
                                </span>
                            ))}
                        </div>

                        <input
                            type="text"
                            className='bg-react-blue border p-2 mb-5 w-full'
                            onKeyDown={handleKeyDown}
                            onChange={(e) => setTagInput(e.target.value)}
                            value={tagInput}
                            placeholder="Tags"
                        />
                        
                        <ReactQuill
                            className='h-72'
                            theme="snow"
                            value={content}
                            modules={modules}
                            formats={formats}
                            placeholder="write your content ...."
                            onChange={handleProcedureContentChange}
                        >
                        </ReactQuill>

                        <div className='h-20 box-content flex flex-col justify-between items-center lg:flex-row lg:justify-between pt-32 md:pt-20'>
                            <span className='flex relative'>
                                <div className='group relative mr-5'>
                                    <button
                                        type="button"
                                        onClick={() => navigate('/dashboard')}
                                        className='border border-white/[0.1] bg-red-500/50 rounded-full w-20 h-10 flex justify-center items-center shadow-md shadow-slate-950 text-white transition-colors duration-700 transform hover:bg-white hover:text-react-blue hover:border-transparent'>
                                        <BsTrash className="text-md" />
                                    </button>

                                    <div className="absolute left-1/2 top-[calc(100%+8px)] transform -translate-x-1/2 px-3 py-2 bg-white text-react-blue text-sm rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 whitespace-nowrap z-50 before:content-[''] before:absolute before:top-[-4px] before:left-1/2 before:transform before:-translate-x-1/2 before:border-4 before:border-transparent before:border-b-white">
                                        Discard
                                    </div>
                                </div>

                                <div className='group relative mr-5'>
                                    <button
                                        type="button"
                                        onClick={togglePreview}
                                        className='border border-white/[0.1] bg-react-blue rounded-full w-20 h-10 flex justify-center items-center shadow-md shadow-slate-950 text-white transition-colors duration-700 transform hover:bg-white hover:text-react-blue hover:border-transparent'>
                                        <BsEye className="text-md" />
                                    </button>

                                    <div className="absolute left-1/2 top-[calc(100%+8px)] transform -translate-x-1/2 px-3 py-2 bg-white text-react-blue text-sm rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 whitespace-nowrap z-50 before:content-[''] before:absolute before:top-[-4px] before:left-1/2 before:transform before:-translate-x-1/2 before:border-4 before:border-transparent before:border-b-white">
                                        Preview
                                    </div>
                                </div>

                                <div className='group relative'>
                                    <button
                                        type="button"
                                        onClick={saveDraft}
                                        className='border border-white/[0.1] bg-yellow-500/50 rounded-full w-20 h-10 flex justify-center items-center shadow-md shadow-slate-950 text-white transition-colors duration-700 transform hover:bg-white hover:text-react-blue hover:border-transparent'>
                                        <RiDraftLine className="text-md" />
                                    </button>

                                    <div className="absolute left-1/2 top-[calc(100%+8px)] transform -translate-x-1/2 px-3 py-2 bg-white text-react-blue text-sm rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 whitespace-nowrap z-50 before:content-[''] before:absolute before:top-[-4px] before:left-1/2 before:transform before:-translate-x-1/2 before:border-4 before:border-transparent before:border-b-white">
                                        Save Draft
                                    </div>
                                </div>
                            </span>

                            <span className='flex'>
                                <button
                                    type="submit"
                                    className='flex justify-center items-center border border-white/[0.1] bg-react-blue rounded-full w-28 h-10 shadow-md shadow-slate-950 text-sm text-center transition-colors duration-700 transform hover:bg-white hover:text-react-blue hover:border-transparent'>
                                    Publish
                                </button>
                            </span>
                        </div>
                    </form>
                </div>

                {showPreview && (
                    <div className="fixed inset-0 z-40 bg-black bg-opacity-50 pointer-events-auto"></div> // Prevents clicks on the create post page
                )}

                {showPreview && (
                    <PreviewPost
                        title={title}
                        author={{ name: "Alan Thomas", profileImageUrl: "alan-profile.JPG" }}
                        coverImage={coverImage}
                        datePublished={new Date().toLocaleDateString()}
                        content={content}
                        onClose={togglePreview}
                    />
                )}

            </div>
        </>
    )
}

export default CreatePost;