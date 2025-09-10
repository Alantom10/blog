import { IoIosTrendingUp } from "react-icons/io";
import { AiOutlineEdit } from "react-icons/ai";
import { BsFileEarmarkText, BsEye, BsBarChart, BsSearch, BsPlus, BsCalendar2, BsThreeDotsVertical, BsTrash } from 'react-icons/bs';
import { useState, useEffect } from 'react';

function Dashboard() {
    const [posts, setPosts] = useState([
        {
            id: 1,
            title: "Understanding React Hooks",
            slug: "understanding-react-hooks",
            author: {
                name: "Alan Thomas",
                image: null
            },
            cover_image: "https://example.com/",
            date_published: "2025-08-27T20:24:52.442000",
            content: "string",
            tags: ["React", "JavaScript"],
            is_published: true
        },
        {
            id: 2,
            title: "Advanced JavaScript Patterns",
            slug: "advanced-javaScript-patterns",
            author: {
                name: "Alan Thomas",
                image: null
            },
            cover_image: "https://example.com/",
            date_published: "2025-08-27T20:24:52.442000",
            content: "string",
            tags: ["JavaScript"],
            is_published: true
        },
        {
            id: 3,
            title: "Building Modern APIs with FastAPI",
            slug: "building-modern-apis-with-fastapi",
            author: {
                name: "Alan Thomas",
                image: null
            },
            cover_image: "https://example.com/",
            date_published: "2025-08-27T20:24:52.442000",
            content: "string",
            tags: ["Python"],
            is_published: false
        },
    ]);
    const [showDropdown, setShowDropdown] = useState(null);
    const [filterStatus, setFilterStatus] = useState('all');
    const [searchTerm, setSearchTerm] = useState('');

    const stats = {
        totalPosts: posts.length,
        publishedPosts: posts.filter(p => p.is_published === true).length,
        draftPosts: posts.filter(p => p.is_published === false).length
    };

    const filteredPosts = posts.filter(post => {
        const matchesSearch = post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
            post.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));

        let matchesStatus = true;
        if (filterStatus !== 'all') {
            matchesStatus = post.is_published === (filterStatus === 'true');
        }

        return matchesSearch && matchesStatus;
    });

    const handleDeletePost = (postId) => {
        if (window.confirm('Are you sure you want to delete this post?')) {
            setPosts(posts.filter(p => p.id !== postId));
        }
        setShowDropdown(null);
    }

    const formatDate = dateString => {
        const date = new Date(dateString);

        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");

        return `${day}-${month}-${year}`;
    }

    const StatCard = ({ title, value, icon: Icon, color = "blue" }) => {
        const colorClasses = {
            blue: "from-blue-600 to-cyan-500",
            green: "from-green-600 to-emerald-500",
            purple: "from-purple-600 to-pink-500",
            orange: "from-orange-600 to-red-500"
        };

        return (
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700/50">
                <div className="flex items-center justify-between">
                    <div>
                        <p className="text-gray-400 text-sm font-medium">{title}</p>
                        <p className="text-2xl font-bold text-white mt-2">{value}</p>
                    </div>
                    <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${colorClasses[color]} flex items-center justify-center`}>
                        <Icon className="w-6 h-6 text-white" />
                    </div>
                </div>
            </div>
        );
    };

    return (
        <>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

                    <StatCard
                        title="Total Posts"
                        value={stats.totalPosts}
                        icon={BsFileEarmarkText}
                        color="blue"
                    />

                    <StatCard
                        title="Published"
                        value={stats.publishedPosts}
                        icon={BsEye}
                        color="green"
                    />

                    <StatCard
                        title="Drafts"
                        value={stats.draftPosts}
                        icon={AiOutlineEdit}
                        color="orange"
                    />
                </div>

                <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700/50">
                    <div className="pt-12 px-12 pb-6 border-b border-gray-700/50">
                        <div className="flex flex-col md:flex-row md:items-center md: justify-between">
                            <h2 className="text-xl font-semibold text-white mb-4 self-center md:self-start">Blog Posts</h2>

                            <div className="flex flex-col md:flex-row gap-4">
                                <div className="relative">
                                    <BsSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                                    <input
                                        type="text"
                                        placeholder="Search posts..."
                                        value={searchTerm}
                                        onChange={(e) => setSearchTerm(e.target.value)}
                                        className="w-100 pl-10 pr-4 py-2 rounded-lg bg-gray-700/50 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400"
                                    />
                                </div>

                                <select
                                    value={filterStatus}
                                    onChange={(e) => setFilterStatus(e.target.value)}
                                    className="px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400"
                                >
                                    <option value="all">All Status</option>
                                    <option value="true">Published</option>
                                    <option value="false">Draft</option>
                                </select>

                                <button className="flex items-center px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-lg hover:from-blue-700 hover:to-blue-600 transition-all duration-200">
                                    <BsPlus className="w-4 h-4 mr-2" />
                                    New Post
                                </button>
                            </div>
                        </div>
                    </div>

                    <div>
                        <table className="min-w-full">
                            <thead className="bg-gray-700/50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Title</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Tags</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Status</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Date</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredPosts.map((post) => (
                                    <tr key={post.id} className="hover:bg-gray-700/20 transition-colors">
                                        <td className="px-6 py-4">
                                            <div className="flex flex-col">
                                                <div className="text-sm font-medium">{post.title}</div>
                                                <div className="text-sm text-gray-400">by {post.author.name}</div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div>
                                                {post.tags.map((tag, index) => (
                                                    <span
                                                        key={index}
                                                        className="text-sm font-semibold text-blue-300 rounded-xl bg-blue-500/20 p-2 mr-2"
                                                    >
                                                        {tag}
                                                    </span>
                                                ))}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`text-sm font-semibold text-green-300 rounded-xl bg-green-500/20 p-2 mr-2 ${post.is_published === true
                                                    ? 'bg-green-500/20 text-green-300'
                                                    : 'bg-yellow-500/20 text-yellow-300'
                                                }`}>
                                                {
                                                    post.is_published === true
                                                        ? 'Published'
                                                        : 'Draft'
                                                }
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className="text-sm flex items-center text-gray-400">
                                                <BsCalendar2 className="inline-flex w-4 h-4 mr-2" />
                                                {formatDate(post.date_published)}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="relative">
                                                <button
                                                    onClick={() => setShowDropdown(showDropdown === post.id ? null : post.id)}
                                                    className="text-gray-400 hover:text-white transition-colors">
                                                    <BsThreeDotsVertical />
                                                </button>

                                                {showDropdown === post.id && (
                                                    <div className="absolute w-48 right-0 mt-2 bg-gray-800 rounded-lg border border-gray-700 z-10">
                                                        <div>
                                                            <button className="text-gray-300 flex items-center px-4 py-2 text-sm hover:bg-gray-700 hover:text-white w-full">
                                                                <AiOutlineEdit className="w-4 h-4 mr-2" />
                                                                Edit Post
                                                            </button>
                                                            <button className="text-gray-300 flex items-center px-4 py-2 text-sm hover:bg-gray-700 hover:text-white w-full">
                                                                <BsEye className="w-4 h-4 mr-2" />
                                                                View Post
                                                            </button>
                                                            <button
                                                                onClick={() => handleDeletePost(post.id)}
                                                                className="text-red-400 flex items-center px-4 py-2 text-sm hover:bg-gray-700 hover:text-red-300 w-full">
                                                                <BsTrash className="w-4 h-4 mr-2" />
                                                                Delete Post
                                                            </button>
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {filteredPosts.length === 0 && (
                        <div className="text-center py-12">
                            <BsFileEarmarkText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                            <h3 className="text-lg font-medium text-gray-300 mb-2">No posts found</h3>
                            <p className="text-gray-400">
                                {searchTerm || filterStatus !== 'all'
                                    ? 'Try adjusting your search or filter criteria.'
                                    : 'Get started by creating your first blog post.'}
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </>
    )
}

export default Dashboard;