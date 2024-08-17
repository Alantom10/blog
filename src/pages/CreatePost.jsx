import { useEffect, useState } from 'react';
import 'quill/dist/quill.snow.css';
import ReactQuill from 'react-quill';
import jsonData from '../data/mock.json';
import PreviewPost from '../components/PreviewPost';

function CreatePost() {
    const [content, setContent] = useState('');
    const [title, setTitle] = useState('');
    const [coverImage, setCoverImage] = useState('');
    const [coverImageName, setCoverImageName] = useState('');
    const [showPreview, setShowPreview] = useState(false);

    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    const handleProcedureContentChange = (content) => {
        setContent(content);
    };

    const handleTitleChange = (e) => {
        setTitle(e.target.value);
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

    const savePost = async (e) => {
        e.preventDefault();
        try {

            const post = {
                title: title,
                author: {
                    name: "Alan Thomas",
                    profileImageUrl: "alan-profile.JPG",
                },
                coverImage: coverImage || '',
                datePublished: new Date().toLocaleDateString(),
                content: content
            };
    
            // Add new post to existing posts
            let updatedPosts = [...jsonData, post];
    
            // Trigger a download of the updated JSON file
            downloadJSON(updatedPosts, "mock.json");  

        } catch (error) {
            console.error("Error parsing content:", error);
        }
    }

    const downloadJSON = (data, filename) => {
        const fileData = JSON.stringify(data, null, 4);
        const blob = new Blob([fileData], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
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

    return(
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
            <div className="max-w-[960px] mx-auto w-full pb-10 md:pb-20 pt-20 box-content">
                <h1 className="text-center text-3xl lg:text-5xl font-semibold py-20 md:pt-40">Create Post</h1>

                

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

                        <div className='border p-2 mb-5 w-full relative flex'>
                            <label 
                                for="upload-photo"
                                className='flex justify-center items-center border border-white bg-react-blue rounded-full w-32 h-9 inline-block'>
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
                            <button 
                                type="button"
                                onClick={togglePreview}
                                className='flex justify-center items-center border border-white/[0.1] bg-react-blue rounded-full w-28 h-9 shadow-md shadow-slate-950 text-sm text-center transition-colors duration-700 transform hover:bg-white hover:text-react-blue hover:border-transparent'>
                                    Preview
                            </button>
                            <button 
                                type="submit"
                                className='flex justify-center items-center border border-white/[0.1] bg-react-blue rounded-full w-28 h-9 shadow-md shadow-slate-950 text-sm text-center transition-colors duration-700 transform hover:bg-white hover:text-react-blue hover:border-transparent'>
                                    Publish
                            </button>
                        </div>

                    </form>
                </div>

                {showPreview && (
                    <div className="fixed inset-0 z-40 bg-black bg-opacity-50 pointer-events-auto"></div> // Prevents clicks on the create post page
                )}

                {showPreview && (
                    <PreviewPost 
                        title={title} 
                        author = {{name: "Alan Thomas", profileImageUrl: "alan-profile.JPG"}}
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