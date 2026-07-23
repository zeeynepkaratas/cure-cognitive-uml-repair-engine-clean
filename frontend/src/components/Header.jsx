import { useState, useEffect } from 'react';
import { useTheme } from '../context/ThemeContext';
import { Sun, Moon, Home, AlertCircle, Activity, BarChart2, Wifi, WifiOff } from 'lucide-react';
import { checkHealth } from '../services/api';

const NAV_ITEMS = [
  { id: 'home',    label: 'Ana Sayfa',    icon: Home },
  { id: 'results', label: 'Sonuçlar',     icon: BarChart2 },
  { id: 'repair',  label: 'Onarım',       icon: Activity },
  { id: 'errors',  label: 'Hata Günlüğü', icon: AlertCircle },
];

const Header = ({ currentPage, onNavigate }) => {
  const { theme, toggleTheme } = useTheme();
  const [backendOnline, setBackendOnline] = useState(null); // null = checking

  useEffect(() => {
    let cancelled = false;
    const check = async () => {
      const result = await checkHealth();
      if (!cancelled) setBackendOnline(result.online);
    };
    check();
    // 30 saniyede bir tekrar kontrol
    const interval = setInterval(check, 30000);
    return () => { cancelled = true; clearInterval(interval); };
  }, []);

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          {/* Logo */}
          <div className="logo" onClick={() => onNavigate('home')} role="button" tabIndex={0} onKeyDown={(e) => e.key === 'Enter' && onNavigate('home')}>
            <h1>CURE</h1>
            <span className="logo-sub">UML Repair</span>
          </div>

          {/* Navigasyon */}
          <nav className="main-nav" aria-label="Ana navigasyon">
            {NAV_ITEMS.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                className={`nav-btn ${currentPage === id ? 'nav-btn--active' : ''}`}
                onClick={() => onNavigate?.(id)}
                aria-current={currentPage === id ? 'page' : undefined}
              >
                <Icon size={16} />
                <span>{label}</span>
              </button>
            ))}
          </nav>

          {/* Sağ kısım: backend durumu + tema */}
          <div className="header-actions">
            {/* Backend sağlık göstergesi */}
            <div className="health-indicator" title={
              backendOnline === null ? 'Backend kontrol ediliyor…' :
              backendOnline ? 'Backend çevrimiçi' : 'Backend çevrimdışı'
            }>
              {backendOnline === null ? (
                <div className="health-dot health-dot--checking" />
              ) : backendOnline ? (
                <Wifi size={15} className="health-online" />
              ) : (
                <WifiOff size={15} className="health-offline" />
              )}
              <span className="health-label">
                {backendOnline === null ? 'Kontrol…' : backendOnline ? 'Çevrimiçi' : 'Çevrimdışı'}
              </span>
            </div>

            {/* Tema toggle */}
            <button
              onClick={toggleTheme}
              className="theme-toggle"
              aria-label="Tema değiştir"
            >
              {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
