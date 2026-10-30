import React, { useState, useEffect } from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { AnalysisRecord, Crop } from '../types';
import { fetchHistory, deleteAnalysisRecord, getPdfDownloadUrl } from '../services/api';
import {
  History as HistoryIcon,
  Search,
  Filter,
  Download,
  Trash2,
  Eye,
  AlertCircle,
  X,
  CheckCircle2,
  FileText
} from 'lucide-react';

interface HistoryPageProps {
  crops: Crop[];
  onViewRecord: (record: AnalysisRecord) => void;
}

export const HistoryPage: React.FC<HistoryPageProps> = ({ crops, onViewRecord }) => {
  const { t, language } = useLanguage();
  const [historyList, setHistoryList] = useState<AnalysisRecord[]>([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [selectedCrop, setSelectedCrop] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [search, setSearch] = useState<string>('');

  // Modal view
  const [activeModalRecord, setActiveModalRecord] = useState<AnalysisRecord | null>(null);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const data = await fetchHistory(selectedCrop, statusFilter);
      setHistoryList(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [selectedCrop, statusFilter]);

  const handleDelete = async (id: string) => {
    if (!window.confirm(t.historyPage.confirmDelete)) return;
    try {
      await deleteAnalysisRecord(id);
      setHistoryList(prev => prev.filter(item => item.id !== id));
      if (activeModalRecord?.id === id) setActiveModalRecord(null);
    } catch (err) {
      alert('Failed to delete report.');
    }
  };

  const filteredHistory = historyList.filter(item =>
    item.id.toLowerCase().includes(search.toLowerCase()) ||
    item.crop_name.toLowerCase().includes(search.toLowerCase()) ||
    item.disease_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-8 pb-12 max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <h1 className="text-2xl sm:text-4xl font-black text-slate-900 tracking-tight">
          {t.historyPage.title}
        </h1>
        <p className="text-xs sm:text-sm text-slate-600">
          {t.historyPage.subtitle}
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-4 sm:p-5">
        <div className="grid grid-cols-1 sm:grid-cols-12 gap-3">
          {/* Keyword Search */}
          <div className="sm:col-span-6 relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by ID, crop name, or disease..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-xs font-medium text-slate-800 bg-white focus:outline-hidden focus:ring-2 focus:ring-forest-500"
            />
          </div>

          {/* Crop Filter */}
          <div className="sm:col-span-3">
            <select
              value={selectedCrop}
              onChange={(e) => setSelectedCrop(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl border border-slate-300 text-xs font-medium text-slate-800 bg-white focus:outline-hidden focus:ring-2 focus:ring-forest-500"
            >
              <option value="all">All Crops</option>
              {crops.map((c) => (
                <option key={c.code} value={c.common_name}>
                  {c.common_name}
                </option>
              ))}
            </select>
          </div>

          {/* Status Filter */}
          <div className="sm:col-span-3">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl border border-slate-300 text-xs font-medium text-slate-800 bg-white focus:outline-hidden focus:ring-2 focus:ring-forest-500"
            >
              <option value="all">{t.historyPage.filterAll}</option>
              <option value="healthy">{t.historyPage.filterHealthy}</option>
              <option value="diseased">{t.historyPage.filterDiseased}</option>
            </select>
          </div>
        </div>
      </div>

      {/* Table / Grid */}
      {loading ? (
        <div className="text-center py-12 text-slate-500 text-xs">
          Loading field records...
        </div>
      ) : filteredHistory.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
          <HistoryIcon className="w-10 h-10 text-slate-300 mx-auto" />
          <h4 className="font-bold text-slate-700 text-sm">
            {t.historyPage.noHistory}
          </h4>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            Uploaded crop leaf analyses will appear here automatically with their complete diagnostic report and downloadable PDF.
          </p>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Preview</th>
                  <th className="py-3 px-4">Analysis ID</th>
                  <th className="py-3 px-4">Timestamp</th>
                  <th className="py-3 px-4">Crop</th>
                  <th className="py-3 px-4">Diagnosis</th>
                  <th className="py-3 px-4">Confidence</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredHistory.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/70 transition-colors">
                    {/* Thumbnail preview */}
                    <td className="py-3 px-4">
                      {item.image_data_url ? (
                        <img
                          src={item.image_data_url}
                          alt="Thumbnail"
                          className="w-10 h-10 object-cover rounded-lg border border-slate-200"
                        />
                      ) : (
                        <div className="w-10 h-10 rounded-lg bg-slate-100 flex items-center justify-center text-slate-400">
                          🍂
                        </div>
                      )}
                    </td>

                    <td className="py-3 px-4 font-mono font-bold text-slate-700">
                      {item.id}
                    </td>

                    <td className="py-3 px-4 text-slate-500">
                      {item.timestamp}
                    </td>

                    <td className="py-3 px-4 font-semibold text-slate-900">
                      {language === 'ta' && item.crop_name_ta ? item.crop_name_ta : item.crop_name}
                    </td>

                    <td className="py-3 px-4">
                      <span className={`inline-block px-2.5 py-0.5 rounded-full font-bold text-[11px] ${
                        item.is_healthy
                          ? 'bg-emerald-100 text-emerald-800'
                          : 'bg-rose-100 text-rose-800'
                      }`}>
                        {language === 'ta' && item.disease_name_ta ? item.disease_name_ta : item.disease_name}
                      </span>
                    </td>

                    <td className="py-3 px-4 font-bold text-slate-800 font-mono">
                      {item.confidence.toFixed(1)}%
                    </td>

                    {/* Action buttons */}
                    <td className="py-3 px-4 text-right space-x-2">
                      <button
                        onClick={() => setActiveModalRecord(item)}
                        className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-[11px] transition-all"
                        title={t.historyPage.viewBtn}
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>{t.historyPage.viewBtn}</span>
                      </button>

                      <a
                        href={getPdfDownloadUrl(item.id)}
                        download
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-forest-50 hover:bg-forest-100 text-forest-800 font-bold text-[11px] border border-forest-200 transition-all"
                        title={t.historyPage.exportBtn}
                      >
                        <Download className="w-3.5 h-3.5 text-forest-600" />
                        <span>PDF</span>
                      </a>

                      <button
                        onClick={() => handleDelete(item.id)}
                        className="inline-flex items-center p-1.5 rounded-lg text-rose-600 hover:bg-rose-50 transition-all"
                        title={t.historyPage.deleteBtn}
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Individual Report Detail Modal */}
      {activeModalRecord && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 space-y-6 max-h-[85vh] overflow-y-auto custom-scrollbar">
            {/* Modal Header */}
            <div className="flex items-start justify-between border-b border-slate-100 pb-4">
              <div>
                <span className="font-mono text-xs font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
                  {activeModalRecord.id}
                </span>
                <h3 className="text-xl font-black text-slate-900 mt-1">
                  {activeModalRecord.crop_name} — {activeModalRecord.disease_name}
                </h3>
                <p className="text-xs text-slate-500">{activeModalRecord.timestamp}</p>
              </div>

              <button
                onClick={() => setActiveModalRecord(null)}
                className="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="space-y-4 text-xs">
              {activeModalRecord.image_data_url && (
                <div className="rounded-2xl overflow-hidden border border-slate-200 max-h-56 bg-slate-900 flex items-center justify-center">
                  <img
                    src={activeModalRecord.image_data_url}
                    alt="Analyzed leaf"
                    className="object-contain max-h-56 w-auto"
                  />
                </div>
              )}

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <span className="text-slate-500 block">Status</span>
                  <strong className={activeModalRecord.is_healthy ? 'text-emerald-700' : 'text-rose-700'}>
                    {activeModalRecord.is_healthy ? 'Healthy Plant' : 'Diseased'}
                  </strong>
                </div>

                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <span className="text-slate-500 block">Model Confidence</span>
                  <strong className="text-slate-900 font-mono">{activeModalRecord.confidence.toFixed(1)}%</strong>
                </div>

                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <span className="text-slate-500 block">Category</span>
                  <strong className="text-slate-900 capitalize">{activeModalRecord.disease_type}</strong>
                </div>
              </div>

              {activeModalRecord.symptoms_summary && (
                <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 space-y-1">
                  <strong className="text-slate-800">Observed Symptoms:</strong>
                  <p className="text-slate-600 leading-relaxed">{activeModalRecord.symptoms_summary}</p>
                </div>
              )}

              {activeModalRecord.guidance && activeModalRecord.guidance.length > 0 && (
                <div className="space-y-2">
                  <strong className="text-slate-800">Verified Treatment Guidelines Provided:</strong>
                  {activeModalRecord.guidance.map((g, idx) => (
                    <div key={idx} className="p-3 bg-emerald-50/60 border border-emerald-200/80 rounded-xl space-y-1">
                      <div className="flex items-center justify-between">
                        <strong className="text-emerald-950">{g.approved_product_name || g.active_ingredient}</strong>
                        <span className="text-[10px] bg-emerald-200 text-emerald-900 px-2 py-0.5 rounded font-bold uppercase">
                          {g.treatment_category}
                        </span>
                      </div>
                      <p className="text-slate-600">{g.dosage_guidance}</p>
                      <p className="text-[11px] text-slate-500 italic">Citation: {g.source_org}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
              <button
                onClick={() => handleDelete(activeModalRecord.id)}
                className="text-rose-600 hover:text-rose-800 font-bold text-xs"
              >
                Delete This Record
              </button>

              <div className="flex items-center gap-2">
                <a
                  href={getPdfDownloadUrl(activeModalRecord.id)}
                  download
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-forest-600 hover:bg-forest-700 text-white font-bold text-xs shadow-xs"
                >
                  <Download className="w-4 h-4" />
                  <span>Download PDF Report</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
