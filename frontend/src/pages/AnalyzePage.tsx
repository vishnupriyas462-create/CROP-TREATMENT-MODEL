import React, { useState } from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { Crop, PredictionResult } from '../types';
import { analyzeCropImage } from '../services/api';
import { ImageUpload } from '../components/ImageUpload';
import { ShieldCheck, Info } from 'lucide-react';

interface AnalyzePageProps {
  crops: Crop[];
  onAnalysisComplete: (result: PredictionResult) => void;
  onOpenDisclaimer: () => void;
}

export const AnalyzePage: React.FC<AnalyzePageProps> = ({
  crops,
  onAnalysisComplete,
  onOpenDisclaimer
}) => {
  const { t } = useLanguage();
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalyze = async (
    file: File,
    cropHint: string,
    district?: string,
    growthStage?: string,
    symptoms?: string
  ) => {
    setIsLoading(true);
    try {
      const result = await analyzeCropImage(file, cropHint, district, growthStage, symptoms);
      setIsLoading(false);
      onAnalysisComplete(result);
    } catch (err) {
      setIsLoading(false);
      throw err;
    }
  };

  const handleSelectSample = async (type: 'healthy' | 'diseased') => {
    setIsLoading(true);
    try {
      const sampleUrl = type === 'healthy' 
        ? '/samples/sample_healthy_tomato.jpg' 
        : '/samples/sample_early_blight_tomato.jpg';
      
      const response = await fetch(sampleUrl);
      if (!response.ok) {
        throw new Error(`Failed to load sample image: ${response.statusText}`);
      }
      const blob = await response.blob();
      const file = new File(
        [blob], 
        type === 'healthy' ? 'healthy_tomato_leaf.jpg' : 'early_blight_tomato_leaf.jpg', 
        { type: 'image/jpeg' }
      );
      await handleAnalyze(
        file,
        'tomato',
        'Salem District',
        'Vegetative',
        type === 'healthy' ? 'Lush uniform foliage' : 'Concentric dark rings on lower leaves'
      );
    } catch (err) {
      console.error('Failed to load sample leaf:', err);
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      {/* Page Header */}
      <div className="text-center space-y-2">
        <h1 className="text-2xl sm:text-4xl font-black text-slate-900 tracking-tight">
          {t.analyze.title}
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 max-w-xl mx-auto">
          {t.analyze.subtitle}
        </p>
      </div>

      {/* Main Upload Box */}
      <ImageUpload
        crops={crops}
        onAnalyze={handleAnalyze}
        isLoading={isLoading}
        onSelectSample={handleSelectSample}
      />

      {/* Trust & Quality Guidelines */}
      <div className="bg-forest-50/70 border border-forest-200/80 rounded-2xl p-5 text-xs text-slate-700 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-start gap-3">
          <Info className="w-5 h-5 text-forest-700 shrink-0 mt-0.5" />
          <div className="space-y-0.5">
            <h4 className="font-bold text-forest-950 text-xs">Photographing Tips for Highest Accuracy:</h4>
            <p className="text-slate-600">
              Ensure good natural daylight, keep the camera 15-20cm away from the leaf, focus on affected lesions, and avoid heavy shadows or blurred backgrounds.
            </p>
          </div>
        </div>
        <button
          onClick={onOpenDisclaimer}
          className="shrink-0 text-forest-800 font-bold hover:underline"
        >
          Safety Disclaimer
        </button>
      </div>
    </div>
  );
};
