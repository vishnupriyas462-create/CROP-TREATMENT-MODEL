import React, { useState } from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { PredictionResult } from '../types';
import { TreatmentCard } from '../components/TreatmentCard';
import { getPdfDownloadUrl, submitFeedback } from '../services/api';
import {
  ShieldAlert,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Download,
  RotateCcw,
  Sparkles,
  Info,
  Bug,
  HelpCircle,
  ThumbsUp,
  ThumbsDown,
  CameraOff,
  UserCheck
} from 'lucide-react';

interface ResultPageProps {
  result: PredictionResult;
  onNewAnalysis: () => void;
  onOpenDisclaimer: () => void;
}

export const ResultPage: React.FC<ResultPageProps> = ({
  result,
  onNewAnalysis,
  onOpenDisclaimer
}) => {
  const { t, language } = useLanguage();
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [feedbackLoading, setFeedbackLoading] = useState(false);

  const handleFeedback = async (type: string) => {
    setFeedbackLoading(true);
    try {
      await submitFeedback({
        analysis_id: result.analysis_id,
        feedback_type: type,
        crop_name: result.crop,
        predicted_disease: result.disease
      });
      setFeedbackSubmitted(true);
    } catch (err) {
      console.error(err);
    } finally {
      setFeedbackLoading(false);
    }
  };

  const isTamil = language === 'ta';
  const cropDisplay = isTamil ? result.crop_ta : result.crop;
  const diseaseDisplay = isTamil ? result.disease_ta : result.disease;
  const symptomsDisplay = isTamil ? result.symptoms_ta : result.symptoms;
  const causesDisplay = isTamil ? result.causes_ta : result.causes;
  const nextStepsDisplay = isTamil ? result.next_steps_ta : result.next_steps;
  const preventionDisplay = isTamil ? result.prevention_ta : result.prevention;

  const confidenceColor =
    result.confidence_pct >= 85
      ? 'text-emerald-600 bg-emerald-50 border-emerald-200'
      : result.confidence_pct >= 60
      ? 'text-amber-600 bg-amber-50 border-amber-200'
      : 'text-rose-600 bg-rose-50 border-rose-200';

  return (
    <div className="max-w-5xl mx-auto space-y-8 pb-16">
      {/* Top Banner & Action Controls */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 pb-5">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="font-mono text-xs font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
                {result.analysis_id}
              </span>
              <span className="text-xs text-slate-400">
                • {result.timestamp}
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
              {t.results.title}
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">
              {t.results.subtitle}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <a
              href={getPdfDownloadUrl(result.analysis_id)}
              download
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-forest-600 hover:bg-forest-700 text-white font-bold text-xs shadow-xs transition-all active:scale-95"
            >
              <Download className="w-4 h-4" />
              <span>{t.results.exportPdf}</span>
            </a>

            <button
              onClick={onNewAnalysis}
              className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs transition-all active:scale-95"
            >
              <RotateCcw className="w-4 h-4" />
              <span>{t.results.runAnother}</span>
            </button>
          </div>
        </div>

        {/* Low Confidence or Uncertainty Alert */}
        {result.is_uncertain && (
          <div className="p-4 bg-amber-50 border-2 border-amber-300 rounded-2xl flex items-start gap-3 text-amber-900 animate-in fade-in">
            <AlertTriangle className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
            <div className="text-xs space-y-1">
              <h4 className="font-bold text-sm text-amber-950">
                {t.results.uncertaintyWarning} (Confidence: {result.confidence_pct}%)
              </h4>
              <p className="leading-relaxed">
                {result.warning_notice || 'Uncertain prediction — upload a clearer image or consult an agricultural expert.'}
              </p>
            </div>
          </div>
        )}

        {/* Primary Diagnosis Card */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
          {/* Uploaded Leaf Image Preview */}
          <div className="md:col-span-4 relative rounded-2xl overflow-hidden border border-slate-200 bg-slate-900 max-h-64 flex items-center justify-center">
            {result.image_preview ? (
              <img
                src={result.image_preview}
                alt="Analyzed Leaf"
                className="object-cover w-full h-64"
              />
            ) : (
              <div className="text-slate-400 p-8 text-center text-xs">
                Leaf Image Processed
              </div>
            )}
            <div className="absolute top-2.5 left-2.5 bg-black/70 backdrop-blur-xs text-white text-[10px] font-mono px-2 py-0.5 rounded-md">
              Target Leaf Scan
            </div>
          </div>

          {/* Diagnostic Metrics and Badges */}
          <div className="md:col-span-8 space-y-4">
            <div>
              <div className="flex flex-wrap items-center gap-2 mb-2">
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-slate-100 text-slate-800 border border-slate-200">
                  {cropDisplay}
                </span>

                <span
                  className={`px-3 py-1 rounded-full text-xs font-bold border ${
                    result.is_healthy
                      ? 'bg-emerald-100 text-emerald-800 border-emerald-200'
                      : 'bg-rose-100 text-rose-800 border-rose-200'
                  }`}
                >
                  {result.is_healthy ? '🌿 ' + t.common.healthy : '⚠️ ' + result.disease_type.toUpperCase()}
                </span>

                {result.severity !== 'None' && (
                  <span className="px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-200">
                    Severity: {result.severity}
                  </span>
                )}
              </div>

              <h2 className="text-2xl sm:text-3xl font-black text-slate-900">
                {diseaseDisplay}
              </h2>
            </div>

            {/* Model Confidence Meter */}
            <div className="bg-slate-50 rounded-2xl p-4 border border-slate-200/80 space-y-2">
              <div className="flex items-center justify-between text-xs font-bold text-slate-700">
                <span className="flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-forest-600" />
                  {t.results.confidence}:
                </span>
                <span className={`px-2.5 py-0.5 rounded-lg border font-mono ${confidenceColor}`}>
                  {result.confidence_pct}% ({result.confidence_level})
                </span>
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-slate-200 rounded-full h-2.5 overflow-hidden">
                <div
                  className={`h-2.5 rounded-full transition-all duration-500 ${
                    result.confidence_pct >= 85
                      ? 'bg-emerald-600'
                      : result.confidence_pct >= 60
                      ? 'bg-amber-500'
                      : 'bg-rose-500'
                  }`}
                  style={{ width: `${Math.min(result.confidence_pct, 100)}%` }}
                ></div>
              </div>

              <p className="text-[11.5px] text-slate-500 italic">
                {result.confidence_interpretation}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* HIGHLIGHTED DEDICATED ACTION PLAN: WHAT THE USER MUST DO */}
      {result.action_plan && (
        <div className={`bg-white rounded-3xl border-2 shadow-md p-6 sm:p-8 space-y-6 ${
          result.is_healthy ? 'border-emerald-500' : 'border-forest-600'
        }`}>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-forest-100 pb-4">
            <div>
              <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-extrabold mb-1.5 ${
                result.is_healthy
                  ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                  : 'bg-rose-100 text-rose-800 border border-rose-300'
              }`}>
                <span>{result.is_healthy ? '🌿' : '⚡'}</span>
                <span>{isTamil ? result.action_plan.urgency_ta : result.action_plan.urgency}</span>
              </div>
              <h3 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
                {result.is_healthy 
                  ? (isTamil ? '🌿 ஆரோக்கியமான பயிர் பராமரிப்பு திட்டம்' : '🌿 Healthy Crop Care & Growth Plan')
                  : t.results.actionPlanTitle}
              </h3>
              <p className="text-xs text-slate-500">
                {result.is_healthy
                  ? (isTamil ? 'பயிரை தொடர்ந்து ஆரோக்கியமாக வைத்திருக்க இந்த வழிமுறைகளைப் பின்பற்றவும்.' : 'Follow these maintenance best practices to maintain optimal foliage vigor and prevent disease onset.')
                  : t.results.actionPlanSub}
              </p>
            </div>

            <a
              href="tel:18001801551"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-forest-600 hover:bg-forest-700 text-white font-bold text-xs shadow-xs shrink-0 active:scale-95 transition-all"
            >
              <span>📞 Kisan Helpline: 1800-180-1551</span>
            </a>
          </div>

          {/* 4-Step Action Timeline */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {/* Step 1: Immediate Field Action */}
            <div className={`border rounded-2xl p-4 space-y-2 ${
              result.is_healthy ? 'bg-emerald-50/70 border-emerald-200' : 'bg-rose-50/70 border-rose-200'
            }`}>
              <div className="flex items-center gap-2">
                <span className={`w-6 h-6 rounded-full text-white font-black text-xs flex items-center justify-center shrink-0 ${
                  result.is_healthy ? 'bg-emerald-600' : 'bg-rose-600'
                }`}>
                  1
                </span>
                <h4 className={`font-bold text-sm ${
                  result.is_healthy ? 'text-emerald-950' : 'text-rose-950'
                }`}>
                  {result.is_healthy 
                    ? (isTamil ? 'படி 1: உடனடி கள கண்காணிப்பு' : 'Step 1: Immediate Field Scouting')
                    : t.results.step1Title}
                </h4>
              </div>
              <p className={`leading-relaxed font-medium pl-8 ${
                result.is_healthy ? 'text-emerald-900' : 'text-rose-900'
              }`}>
                {isTamil ? result.action_plan.step_1_immediate_ta : result.action_plan.step_1_immediate}
              </p>
            </div>

            {/* Step 2: Day 1 Cultural & Biological */}
            <div className="bg-emerald-50/70 border border-emerald-200 rounded-2xl p-4 space-y-2">
              <div className="flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-emerald-600 text-white font-black text-xs flex items-center justify-center shrink-0">
                  2
                </span>
                <h4 className="font-bold text-emerald-950 text-sm">
                  {t.results.step2Title}
                </h4>
              </div>
              <p className="text-emerald-900 leading-relaxed font-medium pl-8">
                {isTamil ? result.action_plan.step_2_biological_cultural_ta : result.action_plan.step_2_biological_cultural}
              </p>
            </div>

            {/* Step 3: Days 2-3 Chemical Application */}
            <div className="bg-blue-50/70 border border-blue-200 rounded-2xl p-4 space-y-2">
              <div className="flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-blue-600 text-white font-black text-xs flex items-center justify-center shrink-0">
                  3
                </span>
                <h4 className="font-bold text-blue-950 text-sm">
                  {t.results.step3Title}
                </h4>
              </div>
              <p className="text-blue-900 leading-relaxed font-medium pl-8">
                {isTamil ? result.action_plan.step_3_chemical_application_ta : result.action_plan.step_3_chemical_application}
              </p>
            </div>

            {/* Step 4: Day 7 Monitoring Checklist */}
            <div className="bg-amber-50/70 border border-amber-200 rounded-2xl p-4 space-y-2">
              <div className="flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-amber-600 text-white font-black text-xs flex items-center justify-center shrink-0">
                  4
                </span>
                <h4 className="font-bold text-amber-950 text-sm">
                  {t.results.step4Title}
                </h4>
              </div>
              <p className="text-amber-900 leading-relaxed font-medium pl-8">
                {isTamil ? result.action_plan.step_4_monitoring_ta : result.action_plan.step_4_monitoring}
              </p>
            </div>
          </div>

          {/* CRITICAL DO-NOTS (WHAT NOT TO DO) */}
          {result.action_plan.critical_donots && result.action_plan.critical_donots.length > 0 && (
            <div className="bg-slate-900 text-white rounded-2xl p-5 space-y-3">
              <div className="flex items-center gap-2 text-rose-400 font-bold text-xs uppercase tracking-wider">
                <AlertTriangle className="w-4 h-4 text-rose-500" />
                <span>{t.results.donotsTitle}</span>
              </div>
              <ul className="space-y-1.5 text-xs text-slate-300">
                {(isTamil ? result.action_plan.critical_donots_ta : result.action_plan.critical_donots).map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-rose-500 font-bold shrink-0">✕</span>
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Pathological Insights Sections */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Symptoms */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-2">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-2">
            <Info className="w-4 h-4 text-forest-600" />
            {t.results.symptomsTitle}
          </h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            {symptomsDisplay}
          </p>
        </div>

        {/* Causes & Environmental Drivers */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-2">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-2">
            <Bug className="w-4 h-4 text-amber-600" />
            {t.results.causesTitle}
          </h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            {causesDisplay}
          </p>
        </div>

        {/* Immediate Next Steps */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-2">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-2 text-forest-800">
            <CheckCircle2 className="w-4 h-4 text-forest-600" />
            {t.results.nextStepsTitle}
          </h3>
          <p className="text-xs text-slate-600 leading-relaxed font-medium">
            {nextStepsDisplay}
          </p>
        </div>

        {/* Prevention & Hygiene */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-2">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-2 text-slate-800">
            <ShieldCheck className="w-4 h-4 text-teal-600" />
            {t.results.preventionTitle}
          </h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            {preventionDisplay}
          </p>
        </div>
      </div>

      {/* Integrated Pest Management (IPM) */}
      <div className="bg-gradient-to-r from-forest-50 to-emerald-50 rounded-2xl border border-forest-200/80 p-6 shadow-xs space-y-2">
        <h3 className="font-bold text-forest-950 text-sm flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-forest-700" />
          {t.results.ipmTitle}
        </h3>
        <p className="text-xs text-forest-900 leading-relaxed">
          {result.ipm}
        </p>
      </div>

      {/* Verified Treatments Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between border-b border-slate-200 pb-3">
          <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-forest-600" />
            {t.results.treatmentsTitle}
          </h3>
          <span className="text-xs text-slate-500 font-medium">
            {result.verified_guidance.length} Verified Solutions
          </span>
        </div>

        {result.verified_guidance.length === 0 ? (
          <div className="p-6 bg-slate-50 border border-slate-200 rounded-2xl text-xs text-slate-600 leading-relaxed">
            {t.results.noTreatments}
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {result.verified_guidance.map((item) => (
              <TreatmentCard key={item.id} item={item} />
            ))}
          </div>
        )}
      </div>

      {/* Alternative Possible Diagnoses */}
      {result.alternatives && result.alternatives.length > 0 && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-3">
          <h4 className="font-bold text-slate-800 text-xs uppercase tracking-wider flex items-center gap-1.5">
            <HelpCircle className="w-4 h-4 text-slate-500" />
            {t.results.alternativesTitle}
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {result.alternatives.map((alt, idx) => (
              <div key={idx} className="p-3 bg-slate-50 rounded-xl border border-slate-200/80 text-xs space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-900">
                    {isTamil ? alt.disease_ta : alt.disease}
                  </span>
                  <span className="font-mono font-bold text-forest-700">
                    {alt.confidence_pct}%
                  </span>
                </div>
                <p className="text-[11px] text-slate-500">
                  {alt.crop} • {alt.disease_type}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Feedback Section */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs text-center space-y-4">
        <div>
          <h4 className="font-bold text-slate-900 text-sm">
            {t.results.feedbackPrompt}
          </h4>
          <p className="text-xs text-slate-500 mt-0.5">
            Feedback is stored in a separate review repository to aid regional agricultural extension refinement.
          </p>
        </div>

        {feedbackSubmitted ? (
          <div className="p-3.5 bg-emerald-50 text-emerald-800 rounded-xl text-xs font-semibold inline-flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            {t.results.feedbackThankYou}
          </div>
        ) : (
          <div className="flex flex-wrap items-center justify-center gap-2.5">
            <button
              onClick={() => handleFeedback('correct')}
              disabled={feedbackLoading}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-emerald-50 hover:text-emerald-800 text-slate-700 text-xs font-semibold border border-slate-200 transition-all active:scale-95"
            >
              <ThumbsUp className="w-3.5 h-3.5 text-emerald-600" />
              {t.results.feedbackCorrect}
            </button>

            <button
              onClick={() => handleFeedback('incorrect')}
              disabled={feedbackLoading}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-rose-50 hover:text-rose-800 text-slate-700 text-xs font-semibold border border-slate-200 transition-all active:scale-95"
            >
              <ThumbsDown className="w-3.5 h-3.5 text-rose-600" />
              {t.results.feedbackIncorrect}
            </button>

            <button
              onClick={() => handleFeedback('poor_image')}
              disabled={feedbackLoading}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-amber-50 hover:text-amber-800 text-slate-700 text-xs font-semibold border border-slate-200 transition-all active:scale-95"
            >
              <CameraOff className="w-3.5 h-3.5 text-amber-600" />
              {t.results.feedbackPoor}
            </button>

            <button
              onClick={() => handleFeedback('expert_required')}
              disabled={feedbackLoading}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-sky-50 hover:text-sky-800 text-slate-700 text-xs font-semibold border border-slate-200 transition-all active:scale-95"
            >
              <UserCheck className="w-3.5 h-3.5 text-sky-600" />
              {t.results.feedbackExpert}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
