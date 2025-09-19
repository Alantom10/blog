import './App.css';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import { Route, Routes, useLocation, matchPath } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import BlogPage from './pages/BlogPage';
import CreatePost from './pages/admin/CreatePost';
import Login from './pages/admin/Login';
import Dashboard from './pages/admin/Dashboard';
import AdminHeader from './components/layout/AdminHeader';

function App() {
  const location = useLocation();

  // List of routes where header/footer should be hidden
  const hideHeaderFooter = ["/login", "/dashboard", "/create-post", "/edit-post/:slug"];
  const showAdminHeader = ["/dashboard", "/create-post", "/edit-post/:slug"];

  const shouldShowHeaderFooter = !hideHeaderFooter.some((pattern) => matchPath(pattern, location.pathname));
  const shouldShowAdminHeader = showAdminHeader.some((pattern) => matchPath(pattern, location.pathname));

  return (
    <>
      {shouldShowHeaderFooter && <Header />}
      {shouldShowAdminHeader && <AdminHeader />}
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/blog/:slug" element={<BlogPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/create-post" element={<CreatePost />} />
          <Route path="/edit-post/:slug" element={<CreatePost />} />
        </Routes>
      </div>
      {shouldShowHeaderFooter && <Footer />}
    </>
  );
}

export default App;
