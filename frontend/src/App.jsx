import './App.css';
import Header from './components/shared/Header';
import Footer from './components/shared/Footer';
import { Route, Routes, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import BlogPage from './pages/BlogPage';
import CreatePost from './pages/admin/CreatePost';
import Login from './pages/admin/Login';
import Dashboard from './pages/admin/Dashboard';
import AdminHeader from './components/shared/AdminHeader';

function App() {
  const location = useLocation();

  // List of routes where header/footer should be hidden
  const hideHeaderFooter = ["/login", "/dashboard", "/create-post"];
  const showAdminHeader = ["/dashboard", "/create-post"];

  const shouldShowHeaderFooter = !hideHeaderFooter.includes(location.pathname);
  const shouldShowAdminHeader = showAdminHeader.includes(location.pathname);

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
