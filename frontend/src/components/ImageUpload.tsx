import React, { useState, useRef } from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { Crop } from '../types';
import {
  UploadCloud,
  Camera,
  Image as ImageIcon,
  X,
  AlertCircle,
  Loader2,
  CheckCircle2,
  Sparkles
} from 'lucide-react';

interface ImageUploadProps {
  crops: Crop[];
  onAnalyze: (file: File, cropHint: string, district?: string, growthStage?: string, symptoms?: string) => Promise<void>;
  isLoading: boolean;
  onSelectSample: (type: 'healthy' | 'diseased') => void;
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  crops,
  onAnalyze,
  isLoading,
  onSelectSample
}) => {
  const { t, language } = useLanguage();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Optional metadata inputs
  const [cropHint, setCropHint] = useState<string>('auto');
  const [district, setDistrict] = useState<string>('');
  const [growthStage, setGrowthStage] = useState<string>('Vegetative');
  const [symptoms, setSymptoms] = useState<string>('');
  const [dragOver, setDragOver] = useState(false);

  const validateAndSetFile = (file: File) => {
    setErrorMsg(null);
    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      setErrorMsg('Invalid file format. Please upload a JPEG, PNG, or WebP leaf photograph.');
      return;
    }

    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      setErrorMsg('Image file size exceeds the 10MB limit. Please upload a compressed photo.');
      return;
    }

    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setErrorMsg(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
    if (cameraInputRef.current) cameraInputRef.current.value = '';
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) {
      setErrorMsg('Please select or capture a crop leaf image before analyzing.');
      return;
    }

    try {
      await onAnalyze(selectedFile, cropHint, district, growthStage, symptoms);
    } catch (err: any) {
      setErrorMsg(err.message || 'Analysis failed. Please check image and try again.');
    }
  };

  return (
    <div className="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 sm:p-8 space-y-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Dropzone / Preview Area */}
        <div>
          {!previewUrl ? (
            <div
              onDragOver={(e) => {
                e.preventDefault();
                setDragOver(true);
              }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center cursor-pointer transition-all duration-200 ${
                dragOver
                  ? 'border-forest-600 bg-forest-50/70 scale-[0.99]'
                  : 'border-slate-300 hover:border-forest-500 bg-slate-50/50 hover:bg-forest-50/20'
              }`}
            >
              <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-forest-100 text-forest-700 flex items-center justify-center shadow-xs">
                <UploadCloud className="w-8 h-8" />
              </div>
              <h4 className="text-base font-bold text-slate-800 mb-1">
                {t.analyze.dragDropTitle}
              </h4>
              <p className="text-xs text-slate-500 mb-4">
                {t.analyze.dragDropSub}
              </p>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center justify-center gap-3">
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    fileInputRef.current?.click();
                  }}
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-white border border-slate-300 text-xs font-semibold text-slate-700 shadow-xs hover:bg-slate-100 transition-all"
                >
                  <ImageIcon className="w-4 h-4 text-forest-600" />
                  Browse Device
                </button>
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    cameraInputRef.current?.click();
                  }}
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-forest-600 hover:bg-forest-700 text-xs font-semibold text-white shadow-xs transition-all"
                >
                  <Camera className="w-4 h-4" />
                  {t.analyze.cameraCapture}
                </button>
              </div>

              {/* Hidden file inputs */}
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                className="hidden"
                onChange={handleFileChange}
              />
              <input
                ref={cameraInputRef}
                type="file"
                accept="image/*"
                capture="environment"
                className="hidden"
                onChange={handleFileChange}
              />
            </div>
          ) : (
            /* Selected Image Preview */
            <div className="relative rounded-2xl overflow-hidden border border-slate-200 bg-slate-900 flex items-center justify-center max-h-96">
              <img
                src={previewUrl}
                alt="Selected Crop Leaf"
                className="object-contain max-h-96 w-auto"
              />
              <div className="absolute top-3 right-3 flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="px-3 py-1.5 rounded-lg bg-black/60 hover:bg-black/80 backdrop-blur-md text-white text-xs font-semibold transition-all"
                >
                  Change
                </button>
                <button
                  type="button"
                  onClick={handleClear}
                  className="p-1.5 rounded-lg bg-rose-600 hover:bg-rose-700 text-white shadow-md transition-all"
                  title={t.analyze.removeImage}
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              <div className="absolute bottom-3 left-3 px-3 py-1 rounded-md bg-black/60 backdrop-blur-xs text-white text-[11px] font-mono">
                {selectedFile?.name} ({(selectedFile ? selectedFile.size / 1024 : 0).toFixed(1)} KB)
              </div>
            </div>
          )}
        </div>

        {/* Quick Sample Selector for Instant Verification */}
        <div className="bg-slate-50 rounded-xl p-3.5 border border-slate-200/80 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-1.5 text-slate-700 font-medium">
            <Sparkles className="w-4 h-4 text-amber-500" />
            <span>{t.analyze.sampleLeaves}</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => onSelectSample('healthy')}
              className="px-3 py-1 rounded-lg bg-white border border-slate-300 hover:border-emerald-500 text-slate-700 font-semibold shadow-2xs hover:bg-emerald-50 transition-all"
            >
              🌿 {t.analyze.healthySample}
            </button>
            <button
              type="button"
              onClick={() => onSelectSample('diseased')}
              className="px-3 py-1 rounded-lg bg-white border border-slate-300 hover:border-rose-500 text-slate-700 font-semibold shadow-2xs hover:bg-rose-50 transition-all"
            >
              🍂 {t.analyze.diseasedSample}
            </button>
          </div>
        </div>

        {/* Form Metadata Fields */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 text-xs">
          {/* Crop Selector */}
          <div>
            <label className="block font-bold text-slate-700 mb-1.5">
              {t.analyze.cropSelectLabel}
            </label>
            <select
              value={cropHint}
              onChange={(e) => setCropHint(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl border border-slate-300 bg-white font-medium text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-forest-500"
            >
              <option value="auto">✨ {t.analyze.cropSelectAuto}</option>
              {crops.map((c) => (
                <option key={c.code} value={c.code}>
                  {language === 'ta' ? `${c.common_name_ta} (${c.common_name})` : c.common_name}
                </option>
              ))}
            </select>
          </div>

          {/* Growth Stage */}
          <div>
            <label className="block font-bold text-slate-700 mb-1.5">
              {t.analyze.growthStageLabel}
            </label>
            <select
              value={growthStage}
              onChange={(e) => setGrowthStage(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl border border-slate-300 bg-white font-medium text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-forest-500"
            >
              <option value="Seedling / Nursery">Seedling / Nursery (நாற்றங்கால்)</option>
              <option value="Vegetative">Vegetative (வளர்ச்சி நிலை)</option>
              <option value="Flowering">Flowering (பூக்கும் பருவம்)</option>
              <option value="Fruiting / Grain Fill">Fruiting / Podding (காய் பிடிக்கும் நிலை)</option>
              <option value="Maturity / Harvest">Pre-Harvest (முதிர்ச்சி நிலை)</option>
            </select>
          </div>

          {/* District / Region */}
          <div className="sm:col-span-2 md:col-span-1">
            <label className="block font-bold text-slate-700 mb-1.5">
              {t.analyze.districtLabel}
            </label>
            <input
              type="text"
              value={district}
              onChange={(e) => setDistrict(e.target.value)}
              placeholder={t.analyze.districtPlaceholder}
              className="w-full px-3 py-2.5 rounded-xl border border-slate-300 bg-white font-medium text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-forest-500"
            />
          </div>
        </div>

        {/* Symptoms observation input */}
        <div>
          <label className="block font-bold text-slate-700 mb-1.5 text-xs">
            {t.analyze.symptomsLabel}
          </label>
          <input
            type="text"
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            placeholder={t.analyze.symptomsPlaceholder}
            className="w-full px-3 py-2.5 rounded-xl border border-slate-300 bg-white text-xs font-medium text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-forest-500"
          />
        </div>

        {/* Error notification */}
        {errorMsg && (
          <div className="p-3.5 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 flex items-start gap-2 animate-in fade-in">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
            <span className="font-medium">{errorMsg}</span>
          </div>
        )}

        {/* Submit Button */}
        <div>
          <button
            type="submit"
            disabled={isLoading || !selectedFile}
            className={`w-full py-3.5 px-6 rounded-2xl text-sm font-bold shadow-md transition-all flex items-center justify-center gap-2 ${
              isLoading || !selectedFile
                ? 'bg-slate-200 text-slate-400 cursor-not-allowed shadow-none'
                : 'bg-forest-600 hover:bg-forest-700 text-white active:scale-[0.99]'
            }`}
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>{t.analyze.analyzing}</span>
              </>
            ) : (
              <>
                <CheckCircle2 className="w-5 h-5" />
                <span>{t.analyze.analyzeBtn}</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
