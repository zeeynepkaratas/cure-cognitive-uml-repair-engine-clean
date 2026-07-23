import { useState, useCallback } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import ResultsPage from './pages/ResultsPage';
import RepairPage from './pages/RepairPage';
import ErrorLogPage from './pages/ErrorLogPage';
import './App.css';

/**
 * Uygulama seviyesinde sayfa kaydı.
 * onNavigate(pageId, data?) çağrısıyla sayfalar arası geçiş + veri aktarımı yapılır.
 */
const App = () => {
  const [currentPage, setCurrentPage] = useState('home');
  const [pageData, setPageData] = useState(null);

  const handleNavigate = useCallback((page, data = null) => {
    setPageData(data);
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage onNavigate={handleNavigate} />;
      case 'results':
        return <ResultsPage data={pageData} onNavigate={handleNavigate} />;
      case 'repair':
        return <RepairPage data={pageData} onNavigate={handleNavigate} />;
      case 'errors':
        return <ErrorLogPage onNavigate={handleNavigate} />;
      default:
        return <HomePage onNavigate={handleNavigate} />;
    }
  };

  return (
    <ThemeProvider>
      <div className="app">
        <Header currentPage={currentPage} onNavigate={handleNavigate} />
        <main className="main-content">
          {renderPage()}
        </main>
        <footer className="footer">
          <div className="container">
            <p>© 2026 CURE — Cognitive UML Repair Engine</p>
          </div>
        </footer>
      </div>
    </ThemeProvider>
  );
};

export default App;
