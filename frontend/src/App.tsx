import React, { useState, useEffect } from 'react';
import { LanguageProvider } from './i18n/LanguageContext';
import { Crop, PredictionResult, AnalysisRecord } from './types';
import { fetchCrops } from './services/api';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { DisclaimerModal } from './components/DisclaimerModal';

import { LandingPage } from './pages/LandingPage';
import { DashboardPage } from './pages/DashboardPage';
import { AnalyzePage } from './pages/AnalyzePage';
import { ResultPage } from './pages/ResultPage';
import { RecommendationsPage } from './pages/RecommendationsPage';
import { LibraryPage } from './pages/LibraryPage';
import { HistoryPage } from './pages/HistoryPage';
import { AdvisoryPage } from './pages/AdvisoryPage';

export const AppContent: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<string>('landing');
  const [crops, setCrops] = useState<Crop[]>([]);
  const [currentResult, setCurrentResult] = useState<PredictionResult | null>(null);
  const [disclaimerOpen, setDisclaimerOpen] = useState<boolean>(false);

  useEffect(() => {
    fetchCrops()
      .then((data) => setCrops(data))
      .catch((err) => console.warn('Using local fallback for crops:', err));
  }, []);

  const navigateTo = (page: string) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleAnalysisComplete = (result: PredictionResult) => {
    setCurrentResult(result);
    navigateTo('result');
  };

  const handleSelectReport = (record: AnalysisRecord) => {
    // Convert AnalysisRecord to PredictionResult structure for deep viewing
    const convertedResult: PredictionResult = {
      success: true,
      analysis_id: record.id,
      timestamp: record.timestamp,
      class_name: record.disease_name,
      crop: record.crop_name,
      crop_ta: record.crop_name_ta || record.crop_name,
      disease: record.disease_name,
      disease_ta: record.disease_name_ta || record.disease_name,
      disease_type: record.disease_type,
      severity: record.is_healthy ? 'None' : 'Moderate',
      is_healthy: record.is_healthy,
      confidence_score: record.confidence / 100,
      confidence_pct: record.confidence,
      confidence_level: record.confidence >= 85 ? 'High' : record.confidence >= 60 ? 'Moderate' : 'Low',
      confidence_interpretation: record.confidence >= 60 ? 'Strong statistical alignment' : 'Uncertain prediction',
      is_uncertain: record.is_uncertain,
      model_version: 'v1.2.0-mobilenetv2',
      model_weights_loaded: true,
      symptoms: record.symptoms_summary || 'Foliar diagnostic record from historical inspection.',
      symptoms_ta: record.symptoms_summary || 'வரலாற்று கள ஆய்வு பதிவு.',
      causes: 'Pathogen identified through optical leaf scan.',
      causes_ta: 'ஒளியியல் ஸ்கேன் மூலம் கண்டறியப்பட்ட காரணி.',
      next_steps: record.notes || 'Continue regular crop scouting and sanitation.',
      next_steps_ta: record.notes || 'பயிர் தூய்மை மற்றும் கண்காணிப்பை தொடரவும்.',
      prevention: 'Maintain balanced fertilization and crop rotation.',
      prevention_ta: 'சமச்சீர் உர மேலாண்மை மற்றும் பயிர் சுழற்சி.',
      ipm: 'Conserve beneficial predators and practice scheduled scouting.',
      alternatives: record.alternatives || [],
      verified_guidance: record.guidance || [],
      has_verified_treatment: (record.guidance || []).length > 0,
      image_preview: record.image_data_url
    };
    setCurrentResult(convertedResult);
    navigateTo('result');
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800">
      <Navbar
        currentPage={currentPage}
        onNavigate={navigateTo}
        onOpenDisclaimer={() => setDisclaimerOpen(true)}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6 sm:pt-8">
        {currentPage === 'landing' && (
          <LandingPage
            onNavigate={navigateTo}
            onOpenDisclaimer={() => setDisclaimerOpen(true)}
          />
        )}

        {currentPage === 'dashboard' && (
          <DashboardPage
            onNavigate={navigateTo}
            onSelectReport={handleSelectReport}
          />
        )}

        {currentPage === 'analyze' && (
          <AnalyzePage
            crops={crops}
            onAnalysisComplete={handleAnalysisComplete}
            onOpenDisclaimer={() => setDisclaimerOpen(true)}
          />
        )}

        {currentPage === 'result' && currentResult && (
          <ResultPage
            result={currentResult}
            onNewAnalysis={() => navigateTo('analyze')}
            onOpenDisclaimer={() => setDisclaimerOpen(true)}
          />
        )}

        {currentPage === 'recommendations' && (
          <RecommendationsPage
            crops={crops}
            onOpenDisclaimer={() => setDisclaimerOpen(true)}
          />
        )}

        {currentPage === 'library' && (
          <LibraryPage
            crops={crops}
            onSelectCropForAnalyze={(cropCode) => {
              navigateTo('analyze');
            }}
          />
        )}

        {currentPage === 'history' && (
          <HistoryPage
            crops={crops}
            onViewRecord={handleSelectReport}
          />
        )}

        {currentPage === 'advisory' && <AdvisoryPage />}
      </main>

      <Footer
        onNavigate={navigateTo}
        onOpenDisclaimer={() => setDisclaimerOpen(true)}
      />

      <DisclaimerModal
        isOpen={disclaimerOpen}
        onClose={() => setDisclaimerOpen(false)}
      />
    </div>
  );
};

export default function App() {
  return (
    <LanguageProvider>
      <AppContent />
    </LanguageProvider>
  );
}
