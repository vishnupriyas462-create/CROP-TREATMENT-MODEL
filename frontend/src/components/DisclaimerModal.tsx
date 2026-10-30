import React from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { ShieldAlert, X, CheckCircle2, AlertTriangle } from 'lucide-react';

interface DisclaimerModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const DisclaimerModal: React.FC<DisclaimerModalProps> = ({ isOpen, onClose }) => {
  const { t } = useLanguage();

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs animate-in fade-in duration-200">
      <div className="bg-white rounded-2xl max-w-xl w-full p-6 shadow-2xl border border-slate-200 space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center shrink-0">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-900">
                {t.common.disclaimerTitle}
              </h3>
              <p className="text-xs text-slate-500">
                Agricultural Decision-Support & Pesticide Safety Guidelines
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 p-1 rounded-lg hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content points */}
        <div className="space-y-3 text-xs text-slate-600 leading-relaxed max-h-[60vh] overflow-y-auto pr-1 custom-scrollbar">
          <div className="p-3.5 bg-amber-50/80 rounded-xl border border-amber-200 text-amber-900 flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-amber-700" />
            <p className="font-medium">
              {t.common.disclaimerNotice}
            </p>
          </div>

          <div className="space-y-2">
            <h4 className="font-bold text-slate-800 text-xs">Core Principles of Agricultural Trust & Safety:</h4>
            
            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-forest-600 shrink-0 mt-0.5" />
              <p>
                <strong>Statistical Model Output:</strong> Prediction percentages reflect image pattern similarity, not a certified laboratory bioassay. Environmental factors like lighting, dust, or multiple overlapping diseases can influence results.
              </p>
            </div>

            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-forest-600 shrink-0 mt-0.5" />
              <p>
                <strong>Never Blindly Spray Chemicals:</strong> Never apply chemical insecticides for fungal or bacterial leaf spots. Always inspect crops for physical insect pests before deciding on chemical interventions.
              </p>
            </div>

            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-forest-600 shrink-0 mt-0.5" />
              <p>
                <strong>Product Label Authorization:</strong> Only purchase and apply crop protection products formally registered with the Central Insecticides Board & Registration Committee (CIBRC) for the specific crop and pest.
              </p>
            </div>

            <div className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-forest-600 shrink-0 mt-0.5" />
              <p>
                <strong>Mandatory Safety Gear:</strong> Always wear certified personal protective equipment (PPE), including face masks, rubber gloves, and eye shields during spray preparation. Strictly observe Pre-Harvest Intervals (PHI).
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-3 border-t border-slate-100 flex items-center justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2.5 rounded-xl bg-forest-600 hover:bg-forest-700 text-white text-xs font-bold shadow-sm transition-all"
          >
            {t.common.understand}
          </button>
        </div>
      </div>
    </div>
  );
};
