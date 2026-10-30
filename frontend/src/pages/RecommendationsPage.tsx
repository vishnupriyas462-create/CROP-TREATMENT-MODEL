import React, { useState, useEffect } from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { GuidanceItem, Crop } from '../types';
import { fetchRecommendations } from '../services/api';
import { TreatmentCard } from '../components/TreatmentCard';
import {
  ShieldCheck,
  Search,
  Filter,
  AlertCircle,
  FlaskConical,
  Award,
  Layers
} from 'lucide-react';

interface RecommendationsPageProps {
  crops: Crop[];
  onOpenDisclaimer: () => void;
}

export const RecommendationsPage: React.FC<RecommendationsPageProps> = ({
  crops,
  onOpenDisclaimer
}) => {
  const { t } = useLanguage();
  const [guidanceList, setGuidanceList] = useState<GuidanceItem[]>([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [selectedCrop, setSelectedCrop] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchRecommendations(selectedCrop, selectedCategory, searchQuery);
      setGuidanceList(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      loadData();
    }, 200);
    return () => clearTimeout(timer);
  }, [selectedCrop, selectedCategory, searchQuery]);

  return (
    <div className="space-y-8 pb-12 max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-forest-100 text-forest-800 text-xs font-bold">
          <Award className="w-3.5 h-3.5 text-forest-700" />
          <span>ICAR & DPPQS Verified Repository</span>
        </div>
        <h1 className="text-2xl sm:text-4xl font-black text-slate-900 tracking-tight">
          {t.treatmentsPage.title}
        </h1>
        <p className="text-xs sm:text-sm text-slate-600">
          {t.treatmentsPage.subtitle}
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-4 sm:p-5 space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-12 gap-3">
          {/* Keyword Search */}
          <div className="sm:col-span-6 relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={t.treatmentsPage.searchPlaceholder}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-xs font-medium text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-forest-500"
            />
          </div>

          {/* Crop Filter */}
          <div className="sm:col-span-3">
            <select
              value={selectedCrop}
              onChange={(e) => setSelectedCrop(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl border border-slate-300 text-xs font-medium text-slate-800 bg-white focus:outline-hidden focus:ring-2 focus:ring-forest-500"
            >
              <option value="all">{t.treatmentsPage.filterCrop}</option>
              {crops.map((c) => (
                <option key={c.code} value={c.code}>
                  {c.common_name}
                </option>
              ))}
            </select>
          </div>

          {/* Category Filter */}
          <div className="sm:col-span-3">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl border border-slate-300 text-xs font-medium text-slate-800 bg-white focus:outline-hidden focus:ring-2 focus:ring-forest-500"
            >
              <option value="all">{t.treatmentsPage.filterCategory}</option>
              <option value="fungicide">{t.treatmentsPage.fungicides}</option>
              <option value="insecticide">{t.treatmentsPage.insecticides}</option>
              <option value="bactericide">{t.treatmentsPage.bactericides}</option>
              <option value="biological">{t.treatmentsPage.biologicals}</option>
              <option value="organic">{t.treatmentsPage.organics}</option>
            </select>
          </div>
        </div>

        {/* Safety Disclaimer Banner */}
        <div className="text-[11.5px] text-slate-500 flex items-center justify-between pt-1 border-t border-slate-100">
          <span>Showing {guidanceList.length} verified records</span>
          <button
            onClick={onOpenDisclaimer}
            className="text-forest-700 hover:text-forest-900 font-semibold underline underline-offset-2"
          >
            Review Safety Standards
          </button>
        </div>
      </div>

      {/* Cards List */}
      {loading ? (
        <div className="text-center py-12 text-slate-500 text-xs font-medium">
          Loading verified agricultural records...
        </div>
      ) : guidanceList.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-8 text-center space-y-2">
          <AlertCircle className="w-8 h-8 text-slate-400 mx-auto" />
          <p className="text-xs text-slate-600 font-medium">
            {t.treatmentsPage.noResults}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {guidanceList.map((item) => (
            <TreatmentCard key={item.id} item={item} />
          ))}
        </div>
      )}
    </div>
  );
};
