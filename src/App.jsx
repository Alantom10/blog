import './App.css';
import Header from './components/shared/Header';
import Footer from './components/shared/Footer';
import { Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import BlogPage from './pages/BlogPage';

function App() {
  return (
    <>
      <Header />
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/blog-page" element={<BlogPage />} />
        </Routes>
      </div>
      <Footer />
    </>
  );
}

export default App;
