import React from 'react';
import { GuidanceItem } from '../types';
import { useLanguage } from '../i18n/LanguageContext';
import {
  ShieldCheck,
  FlaskConical,
  Sprout,
  Clock,
  AlertTriangle,
  ExternalLink,
  BookOpen
} from 'lucide-react';

interface TreatmentCardProps {
  item: GuidanceItem;
}

export const TreatmentCard: React.FC<TreatmentCardProps> = ({ item }) => {
  const { t, language } = useLanguage();

  const categoryStyles = {
    fungicide: {
      badge: 'bg-indigo-100 text-indigo-800 border-indigo-200',
      label: 'Fungicide (பூஞ்சாணக் கொல்லி)'
    },
    insecticide: {
      badge: 'bg-amber-100 text-amber-800 border-amber-200',
      label: 'Insecticide (பூச்சிக்கொல்லி)'
    },
    bactericide: {
      badge: 'bg-purple-100 text-purple-800 border-purple-200',
      label: 'Bactericide (பாக்டீரியா கொல்லி)'
    },
    biological: {
      badge: 'bg-emerald-100 text-emerald-800 border-emerald-200',
      label: 'Biological Control (உயிரியல் முறை)'
    },
    cultural: {
      badge: 'bg-teal-100 text-teal-800 border-teal-200',
      label: 'Cultural Practice (உழவியல் முறை)'
    },
    organic: {
      badge: 'bg-green-100 text-green-800 border-green-200',
      label: 'Organic Method (இயற்கை முறை)'
    }
  }[item.treatment_category] || {
    badge: 'bg-slate-100 text-slate-800 border-slate-200',
    label: item.treatment_category
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200/90 shadow-xs hover:shadow-md transition-all p-5 space-y-4">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-2 border-b border-slate-100 pb-3">
        <div>
          <span className={`inline-block px-2.5 py-1 rounded-full text-[11px] font-bold border ${categoryStyles.badge} mb-1.5`}>
            {categoryStyles.label}
          </span>
          <h4 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <FlaskConical className="w-4 h-4 text-forest-600 shrink-0" />
            {item.approved_product_name || item.active_ingredient || 'Standard Agricultural Treatment'}
          </h4>
          {item.active_ingredient && item.approved_product_name && (
            <p className="text-xs text-slate-500 font-medium">
              Active: <span className="font-semibold text-slate-700">{item.active_ingredient}</span>
            </p>
          )}
        </div>

        {/* Pre-Harvest Interval (PHI) Badge */}
        {item.harvest_waiting_period_days > 0 ? (
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-amber-50 text-amber-900 border border-amber-200 text-xs font-semibold">
            <Clock className="w-3.5 h-3.5 text-amber-600" />
            <span>PHI: {item.harvest_waiting_period_days} {t.treatmentsPage.days}</span>
          </div>
        ) : (
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-emerald-50 text-emerald-900 border border-emerald-200 text-xs font-semibold">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
            <span>0 Days PHI (Eco-Safe)</span>
          </div>
        )}
      </div>

      {/* Target & Dosage */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
        {item.dosage_guidance && (
          <div className="bg-slate-50/80 rounded-xl p-3 border border-slate-100">
            <p className="font-bold text-slate-700 mb-1 flex items-center gap-1.5">
              <span>💧</span> {t.treatmentsPage.dosage}
            </p>
            <p className="text-slate-600 leading-relaxed font-mono text-[11.5px]">
              {item.dosage_guidance}
            </p>
          </div>
        )}

        <div className="bg-emerald-50/60 rounded-xl p-3 border border-emerald-100">
          <p className="font-bold text-emerald-900 mb-1 flex items-center gap-1.5">
            <Sprout className="w-3.5 h-3.5 text-emerald-600" />
            {t.treatmentsPage.nonChemical}
          </p>
          <p className="text-emerald-800 leading-relaxed text-[11.5px]">
            {item.non_chemical_control}
          </p>
        </div>
      </div>

      {/* Safety & PPE Notice */}
      <div className="bg-amber-50/40 rounded-xl p-3 border border-amber-100/80 text-xs flex items-start gap-2 text-slate-700">
        <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold text-slate-900">{t.treatmentsPage.safetyPrecautions}: </span>
          <span>{item.safety_precautions}</span>
        </div>
      </div>

      {/* Citation and Authority */}
      <div className="pt-2 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-[11px] text-slate-500">
        <div className="flex items-center gap-1.5">
          <BookOpen className="w-3.5 h-3.5 text-forest-600" />
          <span>Source: <strong>{item.source_org}</strong> ({item.reference_citation})</span>
        </div>
        {item.source_url && (
          <a
            href={item.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-forest-700 hover:text-forest-900 font-semibold hover:underline"
          >
            <span>Official Guide</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        )}
      </div>
    </div>
  );
};
