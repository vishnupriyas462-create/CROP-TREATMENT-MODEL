import React from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import {
  Sprout,
  ScanEye,
  ShieldCheck,
  Bug,
  History,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  Award,
  Sparkles,
  Leaf
} from 'lucide-react';

interface LandingPageProps {
  onNavigate: (page: string) => void;
  onOpenDisclaimer: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onNavigate, onOpenDisclaimer }) => {
  const { t } = useLanguage();

  return (
    <div className="space-y-16 pb-12">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-8 pb-12 rounded-3xl bg-gradient-to-b from-forest-50/80 via-emerald-50/30 to-white border border-forest-100/60 p-6 sm:p-12">
        <div className="max-w-4xl mx-auto text-center space-y-6">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-forest-100/80 border border-forest-200 text-forest-800 text-xs font-bold tracking-wide">
            <Sparkles className="w-3.5 h-3.5 text-forest-700" />
            <span>{t.hero.badge}</span>
          </div>

          {/* Heading */}
          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black text-slate-900 tracking-tight leading-[1.15]">
            {t.hero.title}
          </h1>

          {/* Subtitle */}
          <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed font-normal">
            {t.hero.subtitle}
          </p>

          {/* Primary & Secondary Action CTAs */}
          <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
            <button
              onClick={() => onNavigate('analyze')}
              className="inline-flex items-center gap-2.5 px-7 py-3.5 rounded-2xl bg-forest-600 hover:bg-forest-700 text-white font-bold text-sm shadow-md hover:shadow-lg active:scale-95 transition-all"
            >
              <ScanEye className="w-5 h-5" />
              <span>{t.hero.analyzeBtn}</span>
              <ArrowRight className="w-4 h-4 ml-0.5" />
            </button>

            <button
              onClick={() => onNavigate('recommendations')}
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-2xl bg-white hover:bg-slate-50 text-slate-700 font-bold text-sm border border-slate-300 shadow-xs hover:shadow-sm active:scale-95 transition-all"
            >
              <ShieldCheck className="w-5 h-5 text-forest-600" />
              <span>{t.hero.exploreBtn}</span>
            </button>
          </div>

          {/* Compliance tag */}
          <p className="text-xs text-forest-800 font-medium flex items-center justify-center gap-1.5 pt-2">
            <Award className="w-4 h-4 text-forest-600" />
            <span>{t.hero.verifiedBadge}</span>
          </p>
        </div>

        {/* Live Interactive Demo Preview Card */}
        <div className="max-w-3xl mx-auto mt-12 bg-white rounded-3xl border border-slate-200 shadow-xl overflow-hidden">
          <div className="bg-slate-900 px-5 py-3 text-white text-xs font-semibold flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>{t.hero.demoTitle}</span>
            </div>
            <span className="font-mono text-emerald-400">MobileNetV2 Engine</span>
          </div>

          <div className="p-6 sm:p-8 grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
            {/* Visual Leaf Specimen */}
            <div className="md:col-span-5 relative rounded-2xl overflow-hidden bg-slate-100 border border-slate-200 flex items-center justify-center h-52">
              <div className="w-full h-full bg-gradient-to-br from-emerald-800 via-green-700 to-emerald-950 flex flex-col items-center justify-center text-white p-4 text-center">
                <Leaf className="w-16 h-16 text-emerald-300 mb-2 drop-shadow-md" />
                <span className="text-xs font-bold bg-black/40 px-2.5 py-1 rounded-full backdrop-blur-xs">
                  Target Spot (Alternaria solani)
                </span>
                <span className="text-[10px] text-emerald-200 mt-1">Concentric ring necrosis</span>
              </div>
              <div className="absolute top-2.5 left-2.5 bg-black/70 backdrop-blur-xs text-white text-[10px] font-mono px-2 py-0.5 rounded-md">
                Tomato Leaf Specimen
              </div>
            </div>

            {/* Diagnostic readout */}
            <div className="md:col-span-7 space-y-3.5 text-left">
              <div>
                <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-rose-100 text-rose-800 border border-rose-200">
                  Fungal Pathogen Detected
                </span>
                <h3 className="text-lg font-extrabold text-slate-900 mt-1">
                  Tomato Early Blight (Alternaria solani)
                </h3>
                <p className="text-xs text-slate-500">
                  Model Confidence: <strong className="text-forest-700">94.2%</strong> (Strong Statistical Alignment)
                </p>
              </div>

              {/* Verified Treatment Pill */}
              <div className="bg-emerald-50/70 rounded-xl p-3 border border-emerald-200/80 text-xs text-slate-700 space-y-1">
                <p className="font-bold text-emerald-900 flex items-center gap-1.5">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                  Verified Fungicide & IPM Guidance
                </p>
                <p className="text-[11.5px] text-slate-600">
                  Mancozeb 75% WP @ 2.5 g/L OR Trichoderma viride biological spray. Strict 7-day pre-harvest interval.
                </p>
              </div>

              <div className="flex items-center justify-between text-xs pt-1">
                <span className="text-slate-500 italic">Citation: TNAU Crop Protection Section 1.2</span>
                <button
                  onClick={() => onNavigate('analyze')}
                  className="font-bold text-forest-700 hover:text-forest-900 hover:underline inline-flex items-center gap-1"
                >
                  Test Your Crop Now →
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="space-y-8">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
            {t.features.title}
          </h2>
          <p className="text-xs sm:text-sm text-slate-600">
            {t.features.subtitle}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Card 1 */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-xs hover:shadow-md transition-all space-y-3">
            <div className="w-12 h-12 rounded-xl bg-emerald-100 text-forest-700 flex items-center justify-center">
              <ScanEye className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-base text-slate-900">
              {t.features.card1Title}
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t.features.card1Desc}
            </p>
          </div>

          {/* Card 2 */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-xs hover:shadow-md transition-all space-y-3">
            <div className="w-12 h-12 rounded-xl bg-teal-100 text-teal-700 flex items-center justify-center">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-base text-slate-900">
              {t.features.card2Title}
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t.features.card2Desc}
            </p>
          </div>

          {/* Card 3 */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-xs hover:shadow-md transition-all space-y-3">
            <div className="w-12 h-12 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center">
              <Bug className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-base text-slate-900">
              {t.features.card3Title}
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t.features.card3Desc}
            </p>
          </div>

          {/* Card 4 */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-xs hover:shadow-md transition-all space-y-3">
            <div className="w-12 h-12 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center">
              <History className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-base text-slate-900">
              {t.features.card4Title}
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t.features.card4Desc}
            </p>
          </div>
        </div>
      </section>

      {/* 3-Step Simple Explanation */}
      <section className="bg-slate-50/80 rounded-3xl border border-slate-200 p-8 sm:p-12 space-y-8">
        <div className="text-center max-w-xl mx-auto space-y-2">
          <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
            {t.workflow.title}
          </h2>
          <p className="text-xs sm:text-sm text-slate-600">
            Engineered for easy, rapid use directly on mobile phones in field conditions.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center space-y-3">
            <div className="w-12 h-12 mx-auto rounded-2xl bg-forest-600 text-white font-black text-lg flex items-center justify-center shadow-sm">
              1
            </div>
            <h3 className="font-bold text-base text-slate-900">
              {t.workflow.step1Title}
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t.workflow.step1Desc}
            </p>
          </div>

          <div className="text-center space-y-3">
            <div className="w-12 h-12 mx-auto rounded-2xl bg-forest-600 text-white font-black text-lg flex items-center justify-center shadow-sm">
              2
            </div>
            <h3 className="font-bold text-base text-slate-900">
              {t.workflow.step2Title}
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t.workflow.step2Desc}
            </p>
          </div>

          <div className="text-center space-y-3">
            <div className="w-12 h-12 mx-auto rounded-2xl bg-forest-600 text-white font-black text-lg flex items-center justify-center shadow-sm">
              3
            </div>
            <h3 className="font-bold text-base text-slate-900">
              {t.workflow.step3Title}
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t.workflow.step3Desc}
            </p>
          </div>
        </div>
      </section>

      {/* Safety Notice Callout */}
      <section className="bg-amber-50/70 border border-amber-200/90 rounded-2xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-6 h-6 text-amber-700 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <h4 className="font-bold text-sm text-amber-950">
              Decision Support Notice for Responsible Farming
            </h4>
            <p className="text-xs text-amber-900 leading-relaxed max-w-2xl">
              AgriGuard AI is designed as a diagnostic companion. Always consult your district Agricultural Extension Officer or KVK specialist before applying chemical remedies.
            </p>
          </div>
        </div>
        <button
          onClick={onOpenDisclaimer}
          className="shrink-0 px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white text-xs font-bold shadow-xs transition-all"
        >
          View Safety Protocol
        </button>
      </section>
    </div>
  );
};
