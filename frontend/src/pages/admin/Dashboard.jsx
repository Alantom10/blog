import { IoIosTrendingUp } from "react-icons/io";
import { AiOutlineEdit } from "react-icons/ai";
import { BsFileEarmarkText, BsEye, BsBarChart, BsSearch, BsPlus } from 'react-icons/bs';

function Dashboard() {

    const StatCard = ({ title, value, icon: Icon, trend, color = "blue" }) => {
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
                        {trend && (
                            <p className="text-green-400 text-sm mt-1 flex items-center">
                                <IoIosTrendingUp className="text-lg mr-2" />
                                {trend}
                            </p>
                        )}
                    </div>
                    <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${colorClasses[color]} flex items-center justify-center`}>
                        <Icon className="w-6 h-6 text-white" />
                    </div>
                </div>
            </div>
        );
    }

    return (
        <>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">

                    <StatCard
                        title="Total Posts"
                        value="3"
                        icon={BsFileEarmarkText}
                        trend="+2 this week"
                        color="blue"
                    />

                    <StatCard
                        title="Published"
                        value="2"
                        icon={BsEye}
                        trend="+1 this week"
                        color="green"
                    />

                    <StatCard
                        title="Total Views"
                        value="2101"
                        icon={BsBarChart}
                        trend="+15.3%"
                        color="purple"
                    />

                    <StatCard
                        title="Drafts"
                        value="1"
                        icon={AiOutlineEdit}
                        trend="+1 this week"
                        color="orange"
                    />
                </div>

                <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700/50">
                    <div className="p-6 border-b border-gray-700/50">
                        <div className="flex flex-col sm:flex-row sm:items-center sm: justify-between">
                            <h2 className="text-xl font-semibold text-white mb-4 sm:mb-0">Blog Posts</h2>

                            <div className="flex flex-col sm:flex-row gap-4">
                                <div className="relative">
                                    <BsSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                                    <input
                                        type="text"
                                        placeholder="Search posts..."
                                        className="pl-10 pr-4 py-2 rounded-lg bg-gray-700/50 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400"
                                    />
                                </div>

                                <select
                                    className="px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400"
                                >
                                    <option value="all">All Status</option>
                                    <option value="published">Published</option>
                                    <option value="draft">Draft</option>
                                </select>

                                <button className="flex items-center px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-lg hover:from-blue-700 hover:to-blue-600 transition-all duration-200">
                                    <BsPlus className="w-4 h-4 mr-2" />
                                    New Post
                                </button>
                            </div>
                        </div>
                    </div>

                    
                </div>
            </div>
        </>
    )
}

export default Dashboard;