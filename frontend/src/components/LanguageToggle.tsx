import React from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { Globe } from 'lucide-react';

export const LanguageToggle: React.FC = () => {
  const { language, setLanguage } = useLanguage();

  return (
    <div className="inline-flex items-center gap-1.5 bg-forest-50 border border-forest-200/80 rounded-full p-1 text-xs font-medium text-forest-900 shadow-sm">
      <Globe className="w-3.5 h-3.5 ml-1.5 text-forest-700" />
      <button
        onClick={() => setLanguage('en')}
        className={`px-2.5 py-1 rounded-full transition-all duration-200 ${
          language === 'en'
            ? 'bg-forest-600 text-white font-semibold shadow-xs'
            : 'text-forest-800 hover:text-forest-950'
        }`}
      >
        English
      </button>
      <button
        onClick={() => setLanguage('ta')}
        className={`px-2.5 py-1 rounded-full transition-all duration-200 ${
          language === 'ta'
            ? 'bg-forest-600 text-white font-semibold shadow-xs'
            : 'text-forest-800 hover:text-forest-950'
        }`}
      >
        தமிழ்
      </button>
    </div>
  );
};
