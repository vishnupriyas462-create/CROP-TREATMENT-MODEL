import React, { useState } from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { Crop } from '../types';
import {
  BookOpen,
  Search,
  Sprout,
  AlertOctagon,
  CloudSun,
  ShieldCheck,
  ChevronDown,
  ChevronUp,
  Layers,
  Sparkles
} from 'lucide-react';

interface LibraryPageProps {
  crops: Crop[];
  onSelectCropForAnalyze: (cropCode: string) => void;
}

export const LibraryPage: React.FC<LibraryPageProps> = ({ crops, onSelectCropForAnalyze }) => {
  const { t, language } = useLanguage();
  const [search, setSearch] = useState('');
  const [expandedCrop, setExpandedCrop] = useState<string | null>('tomato');

  const isTamil = language === 'ta';

  // Comprehensive educational crop profiles
  const CROP_EDUCATIONAL_DETAILS: Record<string, {
    carePractices: string;
    deficiencies: string;
    diseases: { name: string; symptoms: string; env: string; ipm: string }[];
  }> = {
    tomato: {
      carePractices: 'Optimal soil pH 6.0-6.8. Requires 6-8 hours direct sunlight. Space plants 60x45cm for canopy airflow. Stake vines to keep foliage 20cm above soil.',
      deficiencies: 'Blossom End Rot (Calcium deficiency caused by irregular watering); Interveinal chlorosis (Magnesium/Iron deficiency).',
      diseases: [
        {
          name: 'Early Blight (Alternaria solani)',
          symptoms: 'Concentric ring target spots on lower leaves with chlorotic yellow halo.',
          env: 'Warm temperatures (24-29°C) and alternating wet/dry cycles with prolonged leaf wetness.',
          ipm: 'Trichoderma viride seed treatment; staking; drip irrigation; Mancozeb 75% WP @ 2.5 g/L.'
        },
        {
          name: 'Late Blight (Phytophthora infestans)',
          symptoms: 'Greasy water-soaked lesions turning dark purplish-black with white fuzzy sporulation beneath.',
          env: 'Cool, foggy, wet weather (15-22°C, >90% RH).',
          ipm: 'Resistant hybrids (Arka Rakshak); destroy infected vines; Cymoxanil+Mancozeb.'
        },
        {
          name: 'Tomato Yellow Leaf Curl Virus (TYLCV)',
          symptoms: 'Severe stunting, erect growth habit, cupping/curling leaflets with bright yellow margins.',
          env: 'Spread exclusively by sweetpotato whitefly (Bemisia tabaci) in warm dry weather.',
          ipm: '40-mesh insect netting; yellow sticky traps; neem oil 1500 ppm; rogue infected plants.'
        }
      ]
    },
    potato: {
      carePractices: 'Plant certified disease-free tubers. Ensure adequate earthing-up (hilling) at 30 days to prevent tuber exposure to sunlight and tuber moth.',
      deficiencies: 'Hollow heart (excessive nitrogen / erratic water); Potassium deficiency (bronzing of leaf margins).',
      diseases: [
        {
          name: 'Late Blight (Phytophthora infestans)',
          symptoms: 'Water-soaked rapidly expanding foliage lesions; foul odor in severe outbreaks.',
          env: 'Cool spells (12-22°C) with continuous high humidity or misty rain.',
          ipm: 'Plant resistant cultivars (Kufri Himalini, Kufri Girdhari); prophylactic contact sprays; timely dehaulming.'
        },
        {
          name: 'Early Blight (Alternaria solani)',
          symptoms: 'Angular target lesions bounded by veins; premature leaf yellowing.',
          env: 'Intermittent rain and high humidity followed by warm dry winds.',
          ipm: 'Balanced nitrogen fertilizer; 3-year crop rotation; Chlorothalonil 75% WP.'
        }
      ]
    },
    corn: {
      carePractices: 'Deep tillage to bury stubble. Optimum plant population 24,000 plants/acre. Critical irrigation periods: Knee-high, Silking, and Grain filling.',
      deficiencies: 'V-shaped yellowing starting at leaf tips (Nitrogen deficiency); Purpling of seedling leaves (Phosphorus deficiency in cold soils).',
      diseases: [
        {
          name: 'Common Rust (Puccinia sorghi)',
          symptoms: 'Cinnamon brown to reddish pustules on both upper and lower leaf surfaces.',
          env: 'Cool to moderate temperatures (16-25°C) and high relative humidity.',
          ipm: 'Resistant hybrids; early planting; Azoxystrobin + Difenoconazole if >5% leaf area affected.'
        },
        {
          name: 'Northern Corn Leaf Blight (Exserohilum turcicum)',
          symptoms: 'Long elliptical cigar-shaped grayish-green lesions (3-15cm).',
          env: 'Moderate temperatures (18-27°C) and heavy dew.',
          ipm: 'Tolerant hybrids; crop rotation with legumes; Mancozeb 75% WP @ 2.5 g/L.'
        }
      ]
    },
    pepper: {
      carePractices: 'Sandy loam soil with high organic matter. Raised beds with silver plastic mulch to repel thrips and whiteflies.',
      deficiencies: 'Blossom end rot in sweet peppers (Calcium deficit); Upward leaf cupping (Micronutrient imbalance / Boron).',
      diseases: [
        {
          name: 'Bacterial Spot (Xanthomonas campestris)',
          symptoms: 'Small, circular dark spots with water-soaked margins, causing severe defoliation.',
          env: 'Splashing raindrops, overhead sprinkling, and warm weather (24-30°C).',
          ipm: 'Hot water seed soak; Copper Hydroxide 77% WP @ 2 g/L; avoid handling wet plants.'
        }
      ]
    },
    rice: {
      carePractices: 'System of Rice Intensification (SRI) or conventional puddle transplanting. Alternate Wetting and Drying (AWD) water management saves 25% water while improving root aeration.',
      deficiencies: 'Khaira disease (Zinc deficiency: reddish-brown bronze pigmentation on lower leaves); Nitrogen chlorosis.',
      diseases: [
        {
          name: 'Rice Blast (Magnaporthe oryzae)',
          symptoms: 'Spindle-shaped diamond lesions with gray center and brown margin on leaves and panicle neck.',
          env: 'High relative humidity (>90%), nighttime dew, low night temp (20-22°C), high nitrogen.',
          ipm: 'Blast-resistant varieties (CO 51, ADT 53); split nitrogen doses; Tricyclazole 75% WP @ 0.6 g/L.'
        }
      ]
    },
    cotton: {
      carePractices: 'Deep black cotton or well-drained alluvial soil. Maintain 90x60cm spacing. Nipping (terminal bud removal) at 75-80 days checks vegetative rank growth and promotes bolls.',
      deficiencies: 'Magnesium deficiency (Reddening of older leaves between veins while veins remain green).',
      diseases: [
        {
          name: 'Bacterial Blight (Xanthomonas malvacearum)',
          symptoms: 'Angular leaf spots bounded by veinlets; black arm on stems; boll rot.',
          env: 'Heavy rainfall with high humidity (85%) and temperature around 28°C.',
          ipm: 'Acid seed delinting; Copper oxychloride @ 2.5 g/L + Streptocycline 100 ppm.'
        }
      ]
    }
  };

  const filteredCrops = crops.filter(c =>
    c.common_name.toLowerCase().includes(search.toLowerCase()) ||
    c.common_name_ta.includes(search) ||
    c.category.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-8 pb-12 max-w-5xl mx-auto">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <h1 className="text-2xl sm:text-4xl font-black text-slate-900 tracking-tight">
          {t.library.title}
        </h1>
        <p className="text-xs sm:text-sm text-slate-600">
          {t.library.subtitle}
        </p>
      </div>

      {/* Search Input */}
      <div className="relative max-w-md mx-auto">
        <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder={t.library.searchPlaceholder}
          className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-xs font-medium text-slate-800 bg-white focus:outline-hidden focus:ring-2 focus:ring-forest-500 shadow-xs"
        />
      </div>

      {/* Crops Accordion List */}
      <div className="space-y-4">
        {filteredCrops.map((crop) => {
          const isExpanded = expandedCrop === crop.code;
          const details = CROP_EDUCATIONAL_DETAILS[crop.code];

          return (
            <div
              key={crop.code}
              className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden transition-all"
            >
              {/* Accordion Header */}
              <button
                type="button"
                onClick={() => setExpandedCrop(isExpanded ? null : crop.code)}
                className="w-full p-5 sm:p-6 text-left flex items-center justify-between gap-4 hover:bg-slate-50/70 transition-colors"
              >
                <div className="flex items-center gap-3.5">
                  <div className="w-10 h-10 rounded-xl bg-forest-100 text-forest-800 flex items-center justify-center font-bold shrink-0">
                    <Sprout className="w-5 h-5 text-forest-700" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-base font-bold text-slate-900">
                        {isTamil ? crop.common_name_ta : crop.common_name}
                      </h3>
                      <span className="text-[11px] font-mono italic text-slate-400">
                        ({crop.scientific_name})
                      </span>
                    </div>
                    <p className="text-xs text-slate-500">
                      Category: {crop.category} • {crop.description?.slice(0, 80)}...
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className="hidden sm:inline text-xs font-bold text-forest-700 bg-forest-50 px-2.5 py-1 rounded-lg border border-forest-200">
                    {details?.diseases.length || 0} Diseases
                  </span>
                  {isExpanded ? (
                    <ChevronUp className="w-5 h-5 text-slate-400" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-slate-400" />
                  )}
                </div>
              </button>

              {/* Accordion Expanded Body */}
              {isExpanded && (
                <div className="px-5 sm:px-6 pb-6 pt-2 border-t border-slate-100 space-y-5 animate-in fade-in text-xs">
                  {/* Agronomic Best Practices */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-slate-50 rounded-xl p-4 border border-slate-200/80 space-y-1">
                      <h4 className="font-bold text-slate-800 flex items-center gap-1.5">
                        <Sparkles className="w-4 h-4 text-forest-600" />
                        Crop Care & Soil Best Practices
                      </h4>
                      <p className="text-slate-600 leading-relaxed text-[11.5px]">
                        {details?.carePractices || crop.description}
                      </p>
                    </div>

                    <div className="bg-amber-50/60 rounded-xl p-4 border border-amber-200/80 space-y-1">
                      <h4 className="font-bold text-amber-950 flex items-center gap-1.5">
                        <AlertOctagon className="w-4 h-4 text-amber-700" />
                        Common Nutrient Deficiencies & Physiological Disorders
                      </h4>
                      <p className="text-amber-900 leading-relaxed text-[11.5px]">
                        {details?.deficiencies || 'Soil test recommended for balanced NPK fertilization.'}
                      </p>
                    </div>
                  </div>

                  {/* Common Pathogens */}
                  {details?.diseases && details.diseases.length > 0 && (
                    <div className="space-y-3">
                      <h4 className="font-bold text-slate-900 text-sm flex items-center gap-1.5">
                        <BookOpen className="w-4 h-4 text-forest-600" />
                        Major Pathogens & Integrated Protection:
                      </h4>

                      <div className="space-y-3">
                        {details.diseases.map((d, i) => (
                          <div
                            key={i}
                            className="p-4 rounded-xl border border-slate-200 bg-white shadow-2xs space-y-2"
                          >
                            <div className="flex items-center justify-between">
                              <span className="font-bold text-slate-900 text-xs">
                                {d.name}
                              </span>
                              <span className="text-[10.5px] px-2 py-0.5 rounded-md bg-forest-100 text-forest-800 font-semibold">
                                Integrated IPM
                              </span>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-[11.5px] text-slate-600">
                              <div>
                                <strong className="text-slate-800">Symptoms: </strong>
                                {d.symptoms}
                              </div>
                              <div>
                                <strong className="text-slate-800">Conditions: </strong>
                                {d.env}
                              </div>
                              <div>
                                <strong className="text-slate-800">Management: </strong>
                                {d.ipm}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Quick Action Button */}
                  <div className="pt-2 flex justify-end">
                    <button
                      onClick={() => onSelectCropForAnalyze(crop.code)}
                      className="px-4 py-2 rounded-xl bg-forest-600 hover:bg-forest-700 text-white font-bold text-xs shadow-xs transition-all"
                    >
                      Analyze a {crop.common_name} Leaf →
                    </button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
