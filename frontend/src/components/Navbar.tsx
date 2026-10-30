import React, { useState, useEffect } from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { LanguageToggle } from './LanguageToggle';
import { checkBackendHealth } from '../services/api';
import {
  Sprout,
  LayoutDashboard,
  ScanEye,
  BookOpen,
  History,
  ShieldCheck,
  PhoneCall,
  Menu,
  X,
  CircleDot
} from 'lucide-react';

interface NavbarProps {
  currentPage: string;
  onNavigate: (page: string) => void;
  onOpenDisclaimer: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ currentPage, onNavigate, onOpenDisclaimer }) => {
  const { t } = useLanguage();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);

  useEffect(() => {
    checkBackendHealth()
      .then((res) => setBackendOnline(res.status === 'healthy'))
      .catch(() => setBackendOnline(false));
  }, []);

  const navItems = [
    { id: 'landing', label: t.nav.home, icon: Sprout },
    { id: 'dashboard', label: t.nav.dashboard, icon: LayoutDashboard },
    { id: 'analyze', label: t.nav.analyze, icon: ScanEye },
    { id: 'recommendations', label: t.nav.recommendations, icon: ShieldCheck },
    { id: 'library', label: t.nav.library, icon: BookOpen },
    { id: 'history', label: t.nav.history, icon: History },
    { id: 'advisory', label: t.nav.advisory, icon: PhoneCall },
  ];

  const handleNavClick = (id: string) => {
    onNavigate(id);
    setMobileMenuOpen(false);
  };

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <div
            onClick={() => handleNavClick('landing')}
            className="flex items-center gap-2.5 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-forest-600 to-forest-800 flex items-center justify-center text-white shadow-sm group-hover:scale-105 transition-transform">
              <Sprout className="w-6 h-6 text-emerald-200" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-extrabold text-lg text-slate-900 tracking-tight">
                  AgriGuard
                </span>
                <span className="bg-forest-100 text-forest-800 text-[10px] font-bold px-1.5 py-0.5 rounded-sm">
                  AI
                </span>
              </div>
              <p className="text-[11px] font-medium text-slate-500 leading-none">
                {t.tagline}
              </p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id)}
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-semibold transition-all duration-150 ${
                    isActive
                      ? 'bg-forest-50 text-forest-700 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-forest-600' : 'text-slate-400'}`} />
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* Controls: Health indicator, Disclaimer, LanguageToggle */}
          <div className="hidden sm:flex items-center gap-3">
            {/* Live Model API Health Status */}
            <div
              title={backendOnline ? 'PyTorch Backend Connected' : 'Connecting to Backend...'}
              className="flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-medium bg-slate-100 text-slate-600 border border-slate-200"
            >
              <CircleDot
                className={`w-3 h-3 ${
                  backendOnline === true
                    ? 'text-emerald-500 fill-emerald-500'
                    : backendOnline === false
                    ? 'text-amber-500 fill-amber-500'
                    : 'text-slate-400'
                }`}
              />
              <span className="hidden md:inline">
                {backendOnline === true ? 'AI Online' : backendOnline === false ? 'Offline Mode' : 'Connecting'}
              </span>
            </div>

            <button
              onClick={onOpenDisclaimer}
              className="text-[11px] font-medium text-slate-500 hover:text-slate-800 underline underline-offset-2"
            >
              Safety Info
            </button>

            <LanguageToggle />
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center gap-2 lg:hidden">
            <LanguageToggle />
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 focus:outline-hidden"
              aria-label="Toggle Navigation Menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-b border-slate-200 bg-white px-4 pt-2 pb-4 space-y-1 shadow-lg">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentPage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-semibold transition-all ${
                  isActive
                    ? 'bg-forest-50 text-forest-700'
                    : 'text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-forest-600' : 'text-slate-400'}`} />
                {item.label}
              </button>
            );
          })}
          <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Server: {backendOnline ? 'Online (MobileNetV2)' : 'Local Fallback'}</span>
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenDisclaimer();
              }}
              className="underline text-forest-700 font-medium"
            >
              Safety Disclaimer
            </button>
          </div>
        </div>
      )}
    </header>
  );
};
