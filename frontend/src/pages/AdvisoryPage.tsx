import React, { useEffect, useState } from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { AdvisoryContact } from '../types';
import { fetchAdvisoryContacts } from '../services/api';
import {
  PhoneCall,
  ExternalLink,
  Mail,
  MapPin,
  Building2,
  AlertTriangle,
  Award,
  Clock
} from 'lucide-react';

export const AdvisoryPage: React.FC = () => {
  const { t } = useLanguage();
  const [contacts, setContacts] = useState<AdvisoryContact[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdvisoryContacts()
      .then((data) => {
        setContacts(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-8 pb-12 max-w-5xl mx-auto">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-forest-100 text-forest-800 text-xs font-bold">
          <Award className="w-3.5 h-3.5 text-forest-700" />
          <span>Accredited Public Agricultural Helplines</span>
        </div>
        <h1 className="text-2xl sm:text-4xl font-black text-slate-900 tracking-tight">
          {t.advisoryPage.title}
        </h1>
        <p className="text-xs sm:text-sm text-slate-600">
          {t.advisoryPage.subtitle}
        </p>
      </div>

      {/* Emergency Pest Outbreak Notice */}
      <div className="p-5 bg-amber-50 border-2 border-amber-300 rounded-2xl flex items-start gap-3.5 text-amber-950 shadow-xs">
        <AlertTriangle className="w-6 h-6 text-amber-700 shrink-0 mt-0.5" />
        <div className="space-y-1 text-xs leading-relaxed">
          <h4 className="font-bold text-sm text-amber-950">
            Emergency Farm Outbreak Guidance
          </h4>
          <p>{t.advisoryPage.emergencyNotice}</p>
        </div>
      </div>

      {/* Contacts Cards Grid */}
      {loading ? (
        <div className="text-center py-12 text-slate-500 text-xs">
          Loading authorized advisory contacts...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {contacts.map((c) => (
            <div
              key={c.id}
              className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs hover:shadow-md transition-all space-y-4 flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <div className="w-10 h-10 rounded-xl bg-forest-100 text-forest-800 flex items-center justify-center shrink-0">
                    <Building2 className="w-5 h-5 text-forest-700" />
                  </div>
                  <span className="text-[11px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
                    {c.service_type.replace('_', ' ')}
                  </span>
                </div>

                <div>
                  <h3 className="font-bold text-slate-900 text-base leading-snug">
                    {c.organization}
                  </h3>
                  {c.state_region && (
                    <p className="text-xs text-forest-800 font-medium flex items-center gap-1 mt-1">
                      <MapPin className="w-3.5 h-3.5 text-forest-600" />
                      {c.state_region}
                    </p>
                  )}
                </div>

                {c.notes && (
                  <p className="text-xs text-slate-600 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">
                    {c.notes}
                  </p>
                )}
              </div>

              {/* Action Buttons */}
              <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-xs">
                {c.phone && (
                  <a
                    href={`tel:${c.phone.split('/')[0].trim()}`}
                    className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-forest-600 hover:bg-forest-700 text-white font-bold shadow-xs active:scale-95 transition-all"
                  >
                    <PhoneCall className="w-3.5 h-3.5" />
                    <span>{c.phone}</span>
                  </a>
                )}

                {c.website && (
                  <a
                    href={c.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-slate-600 hover:text-forest-700 font-semibold"
                  >
                    <span>{t.advisoryPage.visitPortal}</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
