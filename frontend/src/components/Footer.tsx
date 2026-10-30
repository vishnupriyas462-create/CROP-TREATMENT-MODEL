import React from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { Sprout, Phone, ShieldAlert, Award, ExternalLink } from 'lucide-react';

interface FooterProps {
  onNavigate: (page: string) => void;
  onOpenDisclaimer: () => void;
}

export const Footer: React.FC<FooterProps> = ({ onNavigate, onOpenDisclaimer }) => {
  const { t } = useLanguage();

  return (
    <footer className="bg-slate-900 text-slate-300 pt-12 pb-8 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-10">
          {/* Brand Info */}
          <div className="space-y-4">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-forest-600 flex items-center justify-center text-white">
                <Sprout className="w-5 h-5 text-emerald-100" />
              </div>
              <span className="font-extrabold text-xl text-white tracking-tight">
                AgriGuard <span className="text-emerald-400 text-sm">AI</span>
              </span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Empowering farmers, agronomists, and rural communities with evidence-based leaf disease identification, integrated pest management, and certified guidance.
            </p>
            <div className="flex items-center gap-2 text-xs text-emerald-400">
              <Award className="w-4 h-4" />
              <span>Aligned with ICAR & CIBRC Protocols</span>
            </div>
          </div>

          {/* Quick Navigation */}
          <div>
            <h4 className="text-xs font-bold text-slate-100 uppercase tracking-wider mb-3">
              Application Modules
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <button
                  onClick={() => onNavigate('analyze')}
                  className="hover:text-emerald-400 transition-colors"
                >
                  {t.nav.analyze}
                </button>
              </li>
              <li>
                <button
                  onClick={() => onNavigate('recommendations')}
                  className="hover:text-emerald-400 transition-colors"
                >
                  {t.nav.recommendations}
                </button>
              </li>
              <li>
                <button
                  onClick={() => onNavigate('dashboard')}
                  className="hover:text-emerald-400 transition-colors"
                >
                  {t.nav.dashboard}
                </button>
              </li>
              <li>
                <button
                  onClick={() => onNavigate('library')}
                  className="hover:text-emerald-400 transition-colors"
                >
                  {t.nav.library}
                </button>
              </li>
              <li>
                <button
                  onClick={() => onNavigate('history')}
                  className="hover:text-emerald-400 transition-colors"
                >
                  {t.nav.history}
                </button>
              </li>
            </ul>
          </div>

          {/* Farmer Advisory Helplines */}
          <div>
            <h4 className="text-xs font-bold text-slate-100 uppercase tracking-wider mb-3">
              Farmer Helpline & Support
            </h4>
            <div className="space-y-3">
              <div className="bg-slate-800/80 rounded-xl p-3 border border-slate-700/60">
                <div className="flex items-center gap-2 text-emerald-400 text-xs font-bold mb-1">
                  <Phone className="w-3.5 h-3.5" />
                  Kisan Call Center (All India)
                </div>
                <p className="text-lg font-black text-white tracking-wide">1800-180-1551</p>
                <p className="text-[11px] text-slate-400">Toll-Free, 22 Official Languages, 6AM-10PM</p>
              </div>

              <div className="bg-slate-800/80 rounded-xl p-3 border border-slate-700/60">
                <div className="flex items-center gap-2 text-emerald-400 text-xs font-bold mb-1">
                  <ExternalLink className="w-3.5 h-3.5" />
                  TNAU Agritech Portal
                </div>
                <p className="text-xs text-slate-300">Coimbatore: 0422-6611383</p>
                <p className="text-[11px] text-slate-400">Tamil Nadu Agricultural University</p>
              </div>
            </div>
          </div>

          {/* Safety & Governance */}
          <div>
            <h4 className="text-xs font-bold text-slate-100 uppercase tracking-wider mb-3">
              Safety & Governance
            </h4>
            <p className="text-xs text-slate-400 leading-relaxed mb-3">
              All chemical application guidance requires strict adherence to registered product labels, recommended protective gear, and local pre-harvest intervals.
            </p>
            <button
              onClick={onOpenDisclaimer}
              className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-emerald-400 text-xs font-semibold border border-slate-700 transition-all"
            >
              <ShieldAlert className="w-3.5 h-3.5" />
              Read Safety Disclaimer
            </button>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-6 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-3">
          <p>© {new Date().getFullYear()} AgriGuard AI Platform. Open Decision-Support Initiative.</p>
          <div className="flex items-center gap-4 text-xs">
            <button onClick={onOpenDisclaimer} className="hover:text-slate-300">
              Disclaimer
            </button>
            <button onClick={() => onNavigate('advisory')} className="hover:text-slate-300">
              KVK Directory
            </button>
            <span>v1.2.0 (MobileNetV2)</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
