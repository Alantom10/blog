import { useEffect } from 'react';
import 'quill/dist/quill.snow.css';
import ReactQuill from 'react-quill';

function CreatePost() {
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    var modules = {
        toolbar: [
            [{ size: ["small", false, "large", "huge"] }],
            ["bold", "italic", "underline", "strike", "blockquote"],
            [{ list: "ordered" }, { list: "bullet" }],
            ["link", "image", "code-block"],
            [
                { list: "ordered" },
                { list: "bullet" },
                { indent: "-1" },
                { indent: "+1" },
                { align: [] }
            ],
            [{ "color": ["#000000", "#e60000", "#ff9900", "#ffff00", "#008a00", "#0066cc", "#9933ff", "#ffffff", "#facccc", "#ffebcc", "#ffffcc", "#cce8cc", "#cce0f5", "#ebd6ff", "#bbbbbb", "#f06666", "#ffc266", "#ffff66", "#66b966", "#66a3e0", "#c285ff", "#888888", "#a10000", "#b26b00", "#b2b200", "#006100", "#0047b2", "#6b24b2", "#444444", "#5c0000", "#663d00", "#666600", "#003700", "#002966", "#3d1466", 'custom-color'] }],
        ]
    };

    var formats = [
        "header", "height", "bold", "italic",
        "underline", "strike", "blockquote",
        "list", "color", "bullet", "indent",
        "link", "image", "align", "size", "code-block",
    ];

    const handleProcedureContentChange = (content) => {
    console.log("content---->", content);
    };

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
                    <ReactQuill
                        className='h-72'
                        theme="snow"
                        modules={modules}
                        formats={formats}
                        placeholder="write your content ...."
                        onChange={handleProcedureContentChange}
                    >
                    </ReactQuill>
                </div>

                <div className='flex justify-center lg:justify-end pt-32 md:pt-20'>
                    <button className='flex justify-center items-center border border-white/[0.1] bg-react-blue rounded-full w-28 h-9 shadow-md shadow-slate-950 text-sm text-center transition-colors duration-700 transform hover:bg-white hover:text-react-blue hover:border-transparent'>Publish</button>
                </div>
            </div>
        </>
    )
}

export default CreatePost;