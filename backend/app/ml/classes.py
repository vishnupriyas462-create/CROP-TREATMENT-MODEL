"""
PlantVillage 38 Classes Definition and Multilingual Disease Knowledge Profiles.
Includes detailed clinical symptoms and actionable, step-by-step Farmer Action Plans.
"""

from typing import Dict, Any

PLANTVILLAGE_CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot_Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites_Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

DISEASE_PROFILES = {
    "Tomato___Early_blight": {
        "crop": "Tomato",
        "crop_ta": "தக்காளி",
        "disease": "Early Blight (Alternaria solani)",
        "disease_ta": "முன் பருவ கருகல் நோய்",
        "disease_type": "fungal",
        "severity": "High",
        "is_healthy": False,
        "symptoms": "Dark brown to black spots with characteristic concentric rings ('target board' pattern) on older lower leaves. Leaves yellow around lesions and drop prematurely.",
        "symptoms_ta": "கீழ் இலைகளில் கருமை நிற வளையங்கள் போன்ற புள்ளிகள் தோன்றி, இலைகள் மஞ்சள் நிறமாகி உதிரும்.",
        "causes": "Fungus Alternaria solani. Favored by warm temperatures (24-29°C) and prolonged leaf wetness from rain, heavy dew, or overhead irrigation.",
        "causes_ta": "அல்டர்னேரியா சோலானி பூஞ்சை. மிதமான வெப்பம் மற்றும் அதிக ஈரப்பதம் உள்ள சூழலில் வேகமாக பரவும்.",
        "next_steps": "Remove and destroy severely affected lower foliage. Avoid overhead sprinkler watering. Ensure field air circulation.",
        "next_steps_ta": "பாதிக்கப்பட்ட அடி இலைகளை அகற்றி அழிக்கவும். மேல் தெளிப்பு பாசனத்தை தவிர்க்கவும்.",
        "prevention": "3-4 year crop rotation away from solanaceous crops. Mulch beneath plants to prevent soil splash. Use certified disease-free seeds.",
        "prevention_ta": "தக்காளி பயிரிட்ட நிலத்தில் மாற்றுப் பயிர் சுழற்சி செய்யவும். சொட்டு நீர் பாசனம் பயன்படுத்தவும்.",
        "ipm": "Monitor weekly for early lesions. Apply Trichoderma viride seed/soil treatment. Stake plants to elevate foliage above soil.",
        "action_plan": {
            "urgency": "High — Action Required within 24 to 48 Hours",
            "urgency_ta": "அவசரம் — 24 முதல் 48 மணி நேரத்திற்குள் நடவடிக்கை தேவை",
            "step_1_immediate": "Prune and bag all infected lower foliage within 25 cm from the ground. Burn or bury them outside the field. Sanitize pruning shears with 70% alcohol.",
            "step_1_immediate_ta": "தரையில் இருந்து 25 செ.மீ வரம்பிலுள்ள பாதிக்கப்பட்ட அடி இலைகளை கவாத்து செய்து பையில் இட்டு வயலுக்கு வெளியே எரிக்கவும். கத்தரிக்கோலை தூய்மைப்படுத்தவும்.",
            "step_2_biological_cultural": "Spread straw or organic mulch beneath plants to stop spore splashing from soil. Drench soil around root zone with Trichoderma viride @ 5 g/L.",
            "step_2_biological_cultural_ta": "மண்ணிலிருந்து பூஞ்சை வித்துக்கள் பரவாமல் தடுக்க வைக்கோல் மூடாக்கு இடவும். வேர் பகுதியில் ட்ரைக்கோடெர்மா விரிடி (5 கிராம்/லிட்டர்) கரைத்து ஊற்றவும்.",
            "step_3_chemical_application": "If leaf lesions affect more than 5% of canopy, spray Mancozeb 75% WP @ 2.0-2.5 g/L water (500 g/acre in 200 L water) using a cone nozzle. Observe 7-day Pre-Harvest Interval.",
            "step_3_chemical_application_ta": "பாதிப்பு 5%க்கு மேல் இருந்தால் மேன்கோசெப் 75% WP (2.0-2.5 கிராம்/லிட்டர்) கலந்து காலை அல்லது மாலையில் தெளிக்கவும். அறுவடைக்கு முன் 7 நாட்கள் இடைவெளி விடவும்.",
            "step_4_monitoring": "Re-scout after 5-7 days. Successful treatment will stop spot enlargement, with lesion edges turning crisp and dry. Repeat spray after 10-12 days if wet weather persists.",
            "step_4_monitoring_ta": "5-7 நாட்களுக்கு பின் மீண்டும் கண்காணிக்கவும். புள்ளிகள் பெரிதாகாமல் காய்ந்துவிட்டால் மருந்து வேலை செய்துள்ளது என அறியலாம்.",
            "critical_donots": [
                "DO NOT spray insecticides — this is a fungal disease and insecticides will have zero effect while killing beneficial pollinators.",
                "DO NOT irrigate using overhead sprinklers — keep leaf canopy completely dry by using furrow or drip irrigation.",
                "DO NOT harvest or enter the crop when foliage is wet from morning dew or rain.",
                "DO NOT harvest fruit before the 7-day Pre-Harvest Interval (PHI) elapses."
            ],
            "critical_donots_ta": [
                "பூச்சிக்கொல்லி மருந்துகளை தெளிக்க வேண்டாம் — இது பூஞ்சை நோய், பூச்சிக்கொல்லி பலன் தராது.",
                "இலைகள் நனையும்படி மேல் தெளிப்பு பாசனம் செய்ய வேண்டாம் — சொட்டு நீர் பாசனம் மட்டுமே செய்யவும்.",
                "இலைகளில் பனி அல்லது மழை ஈரம் இருக்கும் போது வயலில் வேலை செய்ய வேண்டாம்.",
                "மருந்து தெளித்து 7 நாட்கள் முடியும் வரை தக்காளியை அறுவடை செய்ய வேண்டாம்."
            ]
        }
    },
    "Tomato___Late_blight": {
        "crop": "Tomato",
        "crop_ta": "தக்காளி",
        "disease": "Late Blight (Phytophthora infestans)",
        "disease_ta": "பின் பருவ கருகல் நோய்",
        "disease_type": "fungal",
        "severity": "Critical",
        "is_healthy": False,
        "symptoms": "Irregular water-soaked greasy greenish-black lesions on leaves and stems. In high humidity, a delicate white fuzzy fungal growth appears on leaf undersides.",
        "symptoms_ta": "இலைகள் மற்றும் தண்டுகளில் நீர் கசிந்த போன்ற கரும்பச்சை புள்ளிகள் தோன்றி, இலையின் கீழ் வெள்ளை நிற பூஞ்சை படியும்.",
        "causes": "Oomycete pathogen Phytophthora infestans. Spreads explosively during cool, wet, foggy weather (15-22°C with >90% relative humidity).",
        "causes_ta": "பைட்டோப்தோரா இன்ஃபெஸ்டன்ஸ் பூஞ்சை. குளிர்ந்த மற்றும் அதிக ஈரப்பதமான காற்றில் மிக வேகமாக பரவும்.",
        "next_steps": "Promptly rogue and incinerate heavily infected plants. Do not compost infected plant parts. Protect surrounding healthy crop.",
        "next_steps_ta": "கடுமையாக பாதிக்கப்பட்ட செடிகளை பிடுங்கி எரிக்கவும். உரக்குழியில் போட வேண்டாம்.",
        "prevention": "Plant resistant cultivars. Avoid planting near potato fields. Maintain wide plant spacing for canopy drying.",
        "prevention_ta": "நோய் எதிர்ப்பு ரகங்களை பயிரிடவும். உருளைக்கிழங்கு வயல்களுக்கு அருகில் நடுதல் தவிர்க்கவும்.",
        "ipm": "Disease forecasting during rainy periods. Preventative copper-based protective sprays as permitted by local advisory.",
        "action_plan": {
            "urgency": "Critical — Emergency Field Intervention within 24 Hours",
            "urgency_ta": "மிக அவசரம் — 24 மணி நேரத்திற்குள் உடனடி நடவடிக்கை அவசியம்",
            "step_1_immediate": "Immediately rogue out completely collapsed or heavily blighted plants. Seal them in airtight plastic bags and incinerate outside the field. Never place in compost pits.",
            "step_1_immediate_ta": "கடுமையாக தாக்கப்பட்ட செடிகளை உடனடியாக வேரோடு பிடுங்கி பையில் அடைத்து வயலுக்கு வெளியே எரிக்கவும். உரக்குழியில் போடவே கூடாது.",
            "step_2_biological_cultural": "Improve field drainage immediately. Stop all nitrogen fertilizer applications, as lush growth accelerates disease virulence.",
            "step_2_biological_cultural_ta": "வயலில் தேங்கியுள்ள நீரை உடனடியாக வடிக்கவும். தழைச்சத்து (யூரியா) இடுவதை உடனே நிறுத்தவும்.",
            "step_3_chemical_application": "Apply Cymoxanil 8% + Mancozeb 64% WP @ 1.5-2.0 g/L OR Metalaxyl 8% + Mancozeb 64% WP @ 2.5 g/L with thorough coverage on lower leaf surfaces. 10-day PHI.",
            "step_3_chemical_application_ta": "சைமோக்சனில் 8% + மேன்கோசெப் 64% WP (1.5-2.0 கிராம்/லிட்டர்) அல்லது மெட்டலாக்ஸில் கூட்டு மருந்தை இலைகளின் அடிப்பகுதியில் படும்படி தெளிக்கவும்.",
            "step_4_monitoring": "Inspect daily for 10 days. If weather remains foggy or drizzly, rotate to Dimethomorph 50% WP @ 1 g/L after 7 days to prevent fungicide resistance.",
            "step_4_monitoring_ta": "10 நாட்களுக்கு தினமும் கண்காணிக்கவும். குளிர் வானிலை நீடித்தால் 7 நாட்களுக்கு பின் மாற்று பூஞ்சாணக் கொல்லியை பயன்படுத்தவும்.",
            "critical_donots": [
                "DO NOT delay spraying — Late Blight can devastate an entire field in 3 to 5 days under cool foggy conditions.",
                "DO NOT throw blighted vines on farm borders or irrigation channels.",
                "DO NOT use overhead sprinklers during high humidity periods."
            ],
            "critical_donots_ta": [
                "மருந்து தெளிக்க தாமதிக்க வேண்டாம் — குளிர்ந்த பனி வானிலையில் 3 முதல் 5 நாட்களில் முழு பயிரையும் அழித்துவிடும்.",
                "பாதிக்கப்பட்ட இலை தழைகளை வரப்புகளிலோ வாய்க்கால்களிலோ எறிய வேண்டாம்.",
                "பனி காலத்தில் மேல் தெளிப்பு பாசனம் செய்ய வேண்டாம்."
            ]
        }
    },
    "Tomato___Bacterial_spot": {
        "crop": "Tomato",
        "crop_ta": "தக்காளி",
        "disease": "Bacterial Spot (Xanthomonas spp.)",
        "disease_ta": "பாக்டீரியா இலைப்புள்ளி நோய்",
        "disease_type": "bacterial",
        "severity": "High",
        "is_healthy": False,
        "symptoms": "Small, dark, greasy, water-soaked circular lesions on foliage, sometimes surrounded by a distinct yellow halo. Defoliation occurs under severe pressure.",
        "symptoms_ta": "இலைகளில் சிறிய எண்ணெய் பசை போன்ற கருப்பு புள்ளிகள் மற்றும் சுற்றிலும் மஞ்சள் வளையம் தோன்றும்.",
        "causes": "Xanthomonas bacteria spread by wind-driven rain, splashing irrigation, and contaminated tools.",
        "causes_ta": "சாந்தோமோனாஸ் பாக்டீரியா. காற்றுடன் கூடிய மழை மற்றும் ஈரம் மூலம் பரவும்.",
        "next_steps": "Sterilize pruning tools between plants with 70% alcohol. Do not enter fields when leaves are wet.",
        "next_steps_ta": "கவாத்து கருவிகளை தூய்மைப்படுத்தவும். இலை ஈரமாக இருக்கும்போது வயலில் நடக்க வேண்டாம்.",
        "prevention": "Certified pathogen-free seed; hot-water seed treatment at 50°C for 25 min; crop rotation.",
        "prevention_ta": "வெந்நீர் விதை நேர்த்தி செய்யப்பட்ட சான்றளிக்கப்பட்ட விதைகளை பயன்படுத்தவும்.",
        "ipm": "Copper bactericide combined with Mancozeb per university protocol.",
        "action_plan": {
            "urgency": "High — Action within 48 Hours",
            "urgency_ta": "அவசரம் — 48 மணி நேரத்திற்குள் நடவடிக்கை தேவை",
            "step_1_immediate": "Strict quarantine: Keep farm laborers out of wet fields. Bacteria spread by touching wet leaves. Disinfect all pruning tools with 70% isopropyl alcohol.",
            "step_1_immediate_ta": "இலைகள் ஈரமாக இருக்கும்போது பணியாளர்கள் வயலுக்குள் செல்வதை தடுக்கவும். கருவிகளை ஆல்கஹால் கொண்டு கிருமி நீக்கம் செய்யவும்.",
            "step_2_biological_cultural": "Foliar spray with Pseudomonas fluorescens bio-formulation @ 5 g/L water to colonize leaf surface and suppress bacterial colonization.",
            "step_2_biological_cultural_ta": "சியூடோமோனாஸ் ஃப்ளோரசன்ஸ் உயிரியல் மருந்தை (5 கிராம்/லிட்டர்) இலைகளில் தெளித்து பாக்டீரியா வளர்ச்சியை கட்டுப்படுத்தவும்.",
            "step_3_chemical_application": "Spray Copper Hydroxide 53.8% DF @ 2.0 g/L OR Copper Oxychloride 50% WP @ 2.5 g/L. If recommended by university extension, add Streptocycline @ 0.5 g/10 L water.",
            "step_3_chemical_application_ta": "காப்பர் ஹைட்ராக்சைடு (2 கிராம்/லிட்டர்) அல்லது காப்பர் ஆக்ஸிகுளோரைடு (2.5 கிராம்/லிட்டர்) மருந்தை காலை வேளையில் தெளிக்கவும்.",
            "step_4_monitoring": "Check new tender foliage after 7 days. New leaves should emerge free of greasy dark specks.",
            "step_4_monitoring_ta": "7 நாட்களுக்கு பின் புதிய தளிர்களை பார்க்கவும்; புதிய இலைகளில் எண்ணெய் போன்ற கரும்புள்ளிகள் இருக்கக் கூடாது.",
            "critical_donots": [
                "DO NOT spray conventional fungicides alone — bacterial pathogens are immune to standard fungal-only chemicals.",
                "DO NOT use high-pressure sprayers that bruise leaf tissue and create entry wounds for bacteria.",
                "DO NOT prune or pinch sucker shoots during wet or overcast weather."
            ],
            "critical_donots_ta": [
                "சாதாரண பூஞ்சாண மருந்துகளை மட்டும் தெளிக்க வேண்டாம் — அவை பாக்டீரியாவை அழிக்காது.",
                "இலைகளில் காயம் ஏற்படுத்தும் அதிக அழுத்த தெளிப்பான்களை பயன்படுத்த வேண்டாம்.",
                "மழை அல்லது மேகமூட்டமான நாட்களில் கவாத்து பணிகளை செய்ய வேண்டாம்."
            ]
        }
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato",
        "crop_ta": "தக்காளி",
        "disease": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "disease_ta": "தக்காளி இலை சுருட்டு வைரஸ்",
        "disease_type": "viral",
        "severity": "Critical",
        "is_healthy": False,
        "symptoms": "Severe plant stunting, erect growth habit, cupping and curling of leaflets with prominent interveinal chlorosis (yellowing) and flower drop.",
        "symptoms_ta": "செடி வளர்ச்சி குன்றுதல், இலைகள் மேல்நோக்கி சுருண்டு மஞ்சள் நிறமாதல் மற்றும் பூக்கள் கொட்டுதல்.",
        "causes": "Begomovirus transmitted exclusively by the sweetpotato whitefly (Bemisia tabaci). Not seed-transmitted.",
        "causes_ta": "வெள்ளை ஈ (Bemisia tabaci) மூலம் பரவும் வைரஸ் நோய். விதையால் பரவாது.",
        "next_steps": "Immediately rogue out symptomatic plants; install yellow sticky traps to detect and trap whitefly vectors.",
        "next_steps_ta": "பாதிக்கப்பட்ட செடிகளை உடனே பிடுங்கி அழிக்கவும்; மஞ்சள் ஒட்டும் பொறிகளை வைக்கவும்.",
        "prevention": "Grow TYLCV-resistant hybrids; install 40-50 mesh insect-proof nets in nurseries; reflective silver mulches.",
        "prevention_ta": "நோய் எதிர்ப்பு ஒட்டு ரகங்களை பயிரிடவும்; நாற்றங்காலில் பூச்சி வலை அமைக்கவும்.",
        "ipm": "Manage vector whiteflies using neem seed kernel extract (NSKE 5%) or approved systemic insecticides strictly at nursery stage.",
        "action_plan": {
            "urgency": "Critical — Immediate Vector Management Required",
            "urgency_ta": "மிக அவசரம் — வெள்ளை ஈக்களை கட்டுப்படுத்த உடனடி நடவடிக்கை தேவை",
            "step_1_immediate": "Rogue out every symptomatic stunted plant immediately and bury them. Viruses cannot be cured once inside the vascular plant tissue.",
            "step_1_immediate_ta": "வைரஸ் தாக்கிய சுருங்கிய செடிகளை உடனடியாக வேரோடு பிடுங்கி மண்ணில் புதைக்கவும். வைரஸ் தாக்கிய செடியை குணப்படுத்த முடியாது.",
            "step_2_biological_cultural": "Erect 15-20 bright yellow sticky traps per acre at canopy level to monitor and trap adult whiteflies. Lay silver reflective mulch along rows.",
            "step_2_biological_cultural_ta": "ஏக்கருக்கு 15-20 மஞ்சள் ஒட்டும் பொறிகளை பயிர் உயரத்தில் கட்டி வெள்ளை ஈக்களை பிடிக்கவும். வெள்ளி நிற மூடாக்கு அமைக்கவும்.",
            "step_3_chemical_application": "Direct targeted spray at leaf undersides against whiteflies: Azadirachtin 1% (10,000 ppm) @ 2 ml/L water OR approved vector-targeted insecticide (e.g. Imidacloprid 17.8% SL @ 0.3 ml/L at early stage).",
            "step_3_chemical_application_ta": "இலைகளின் அடியில் வெள்ளை ஈக்கள் மீது படும்படி வேப்பெண்ணெய் கரைசல் (10,000 ppm) 2 மி.லி/லிட்டர் அல்லது பரிந்துரைக்கப்பட்ட பூச்சிக்கொல்லி தெளிக்கவும்.",
            "step_4_monitoring": "Inspect yellow sticky traps every 3 days. Whitefly trap counts should fall below 2 per trap per day.",
            "step_4_monitoring_ta": "மஞ்சள் பொறிகளை 3 நாட்களுக்கு ஒருமுறை பார்த்து வெள்ளை ஈக்களின் எண்ணிக்கை குறைந்துள்ளதா என கண்காணிக்கவும்.",
            "critical_donots": [
                "DO NOT attempt to spray fungicides — fungi do not cause leaf curl virus.",
                "DO NOT allow symptomatic plants to remain in the field — they serve as virus reservoirs infecting healthy neighboring plants.",
                "DO NOT spray chemical insecticides during peak daylight hours when honeybees are pollinating."
            ],
            "critical_donots_ta": [
                "பூஞ்சாண மருந்துகளை தெளிக்க வேண்டாம் — இது பூஞ்சை நோய் அல்ல.",
                "தாக்கப்பட்ட செடிகளை வயலில் விட வேண்டாம் — அவை மற்ற ஆரோக்கியமான செடிகளுக்கும் நோயை பரப்பும்.",
                "தேனீக்கள் நடமாட்டம் உள்ள பகல் வேளையில் ரசாயன மருந்துகளை தெளிக்க வேண்டாம்."
            ]
        }
    },
    "Tomato___healthy": {
        "crop": "Tomato",
        "crop_ta": "தக்காளி",
        "disease": "Healthy Plant",
        "disease_ta": "ஆரோக்கியமான பயிர்",
        "disease_type": "healthy",
        "severity": "None",
        "is_healthy": True,
        "symptoms": "Vibrant green, uniform leaf color with no chlorosis, necroses, lesions, or webbing. Vigorous foliage structure.",
        "symptoms_ta": "இலைகள் பசுமையாகவும், புள்ளிகள் அல்லது நோய் தாக்குதல் இன்றி ஆரோக்கியமாக உள்ளன.",
        "causes": "Proper nutrition, optimal soil moisture, and effective cultural practices.",
        "causes_ta": "சரியான உர மேலாண்மை மற்றும் பாசன பராமரிப்பு.",
        "next_steps": "Continue regular pest scouting twice a week. Maintain balanced fertigation (N-P-K + micronutrients).",
        "next_steps_ta": "வழக்கமான பயிர் கண்காணிப்பை தொடரவும்; சமச்சீர் உரங்களை இடவும்.",
        "prevention": "Maintain soil health with organic compost; practice scheduled crop rotation.",
        "prevention_ta": "இயற்கை மக்கிய உரம் இட்டு மண் வளத்தை பாதுகாக்கவும்.",
        "ipm": "Beneficial predator conservation; preventive yellow/blue sticky trap installation.",
        "action_plan": {
            "urgency": "Routine — Preventative Maintenance",
            "urgency_ta": "வழக்கமான பராமரிப்பு — தடுப்பு பாதுகாப்பு முறைகள்",
            "step_1_immediate": "No chemical pesticide intervention needed. Continue scouting crop rows twice weekly, especially examining leaf undersides.",
            "step_1_immediate_ta": "ரசாயன மருந்துகள் தேவையில்லை. வாரத்திற்கு இருமுறை பயிரை கண்காணிக்கவும்.",
            "step_2_biological_cultural": "Maintain regular drip irrigation scheduling and apply well-decomposed farmyard manure or vermicompost to preserve rhizosphere vitality.",
            "step_2_biological_cultural_ta": "வழக்கமான சொட்டு நீர் பாசனம் மற்றும் மண்புழு உரம் இட்டு வேர் மண்டல ஆரோக்கியத்தை பராமரிக்கவும்.",
            "step_3_chemical_application": "No chemical application warranted. Zero chemical residue protects harvest value and soil microbiome.",
            "step_3_chemical_application_ta": "எந்த ரசாயன மருந்தும் தேவையில்லை.",
            "step_4_monitoring": "Re-inspect weekly during rainy spells for any emerging leaf spots or thrip/mite feeding marks.",
            "step_4_monitoring_ta": "மழைக்காலங்களில் இலைகளில் புதிய புள்ளிகள் தோன்றுகிறதா என வாரம் ஒருமுறை கவனிக்கவும்.",
            "critical_donots": [
                "DO NOT apply preventative synthetic pesticides needlessly — overuse destroys predatory spiders and beneficial insects.",
                "DO NOT over-fertilize with excessive nitrogen, which makes leaves excessively succulent and susceptible to blight.",
                "DO NOT let irrigation water stand stagnantly at stem bases."
            ],
            "critical_donots_ta": [
                "தேவையின்றி ரசாயன மருந்துகளை தெளிக்க வேண்டாம் — இது நன்மை செய்யும் பூச்சிகளை அழித்துவிடும்.",
                "அதிகப்படியான யூரியா இட வேண்டாம் — அது இலைகளை நோய்களுக்கு இரையாக்கும்.",
                "செடியின் தண்டு பகுதியில் தண்ணீர் தேங்க விட வேண்டாம்."
            ]
        }
    },
    "Potato___Late_blight": {
        "crop": "Potato",
        "crop_ta": "உருளைக்கிழங்கு",
        "disease": "Late Blight (Phytophthora infestans)",
        "disease_ta": "பின் பருவ கருகல் நோய்",
        "disease_type": "fungal",
        "severity": "Critical",
        "is_healthy": False,
        "symptoms": "Water-soaked dark lesions rapidly expanding across leaves, petioles, and stems. White downy sporulation on lower leaf surface under humid conditions. Foul odor in advanced stages.",
        "symptoms_ta": "இலைகளில் நீர் கசிந்த புள்ளிகள் வேகமாக பரவி, கீழ் பகுதியில் வெண் தூவல் பூஞ்சை தோன்றி பயிர் அழுகும்.",
        "causes": "Phytophthora infestans. Driven by temperatures of 12-22°C with continuous relative humidity >90%.",
        "causes_ta": "பைட்டோப்தோரா இன்ஃபெஸ்டன்ஸ். குளிர் மற்றும் பனி மூட்டமான சூழலில் மிக வேகமாக தாக்கும்.",
        "next_steps": "Destruction of infected foliage before harvesting tubers; do not harvest during wet soil conditions.",
        "next_steps_ta": "அறுவடைக்கு முன் தாக்கப்பட்ட இலைகளை அழிக்கவும்; ஈரமான மண்ணில் அறுவடை செய்ய வேண்டாம்.",
        "prevention": "Plant resistant cultivars (e.g. Kufri Girdhari, Kufri Himalini in India); destroy volunteer potato plants.",
        "prevention_ta": "குப்ரி போன்ற நோய் எதிர்ப்பு விதைக்கிழங்குகளை தேர்வு செய்யவும்.",
        "ipm": "Prophylactic sprays of Mancozeb or metalaxyl-based fungicides per CPRI / ICAR protocol.",
        "action_plan": {
            "urgency": "Critical — Action Required within 24 Hours",
            "urgency_ta": "மிக அவசரம் — 24 மணி நேரத்திற்குள் நடவடிக்கை தேவை",
            "step_1_immediate": "Inspect hill slopes and low-lying hollows where fog gathers. Rogue out and bury isolated infected plants.",
            "step_1_immediate_ta": "பனி தேங்கும் தாழ்வான பகுதிகளை கண்காணித்து தாக்கப்பட்ட செடிகளை உடனே புதைக்கவும்.",
            "step_2_biological_cultural": "If tubers are mature (>75 days), immediately perform dehaulming (cut haulms 10-12 days before tuber lifting) to stop spore movement into tubers.",
            "step_2_biological_cultural_ta": "கிழங்குகள் முதிர்ச்சி அடைந்திருந்தால் இலைகளை அறுத்து அகற்றி கிழங்கு அழுகுவதை தடுக்கவும்.",
            "step_3_chemical_application": "Foliar spray with Dimethomorph 50% WP @ 1.0 g/L OR Fenamidone 10% + Mancozeb 50% WG @ 2.5 g/L with complete leaf canopy wetting.",
            "step_3_chemical_application_ta": "டைமெத்தோமார்ப் (1 கிராம்/லிட்டர்) அல்லது பெனாமிடோன் கூட்டு மருந்தை இலைகள் நனையும்படி தெளிக்கவும்.",
            "step_4_monitoring": "Scout daily. Repeat spray after 7-10 days if foggy cold weather persists.",
            "step_4_monitoring_ta": "தினமும் கண்காணிக்கவும். குளிர் வானிலை நீடித்தால் 7-10 நாட்களுக்கு பின் மீண்டும் தெளிக்கவும்.",
            "critical_donots": [
                "DO NOT harvest tubers in wet soil — wet digging inoculates tubers with late blight rot.",
                "DO NOT store harvested tubers showing brown surface depressions with healthy potatoes."
            ],
            "critical_donots_ta": [
                "மண் ஈரமாக இருக்கும் போது கிழங்குகளை தோண்டி எடுக்க வேண்டாம்.",
                "அழுகல் கண்ட கிழங்குகளை நல்ல உருளைக்கிழங்குகளுடன் சேர்த்து சேமிக்க வேண்டாம்."
            ]
        }
    },
    "Potato___Early_blight": {
        "crop": "Potato",
        "crop_ta": "உருளைக்கிழங்கு",
        "disease": "Early Blight (Alternaria solani)",
        "disease_ta": "முன் பருவ கருகல் நோய்",
        "disease_type": "fungal",
        "severity": "High",
        "is_healthy": False,
        "symptoms": "Brown, circular to oval target-like spots with concentric rings on foliage. Lesions restricted by veins.",
        "symptoms_ta": "இலைகளில் வட்ட வடிவ வளைய புள்ளிகள் தோன்றி, இலைகள் பழுப்பு நிறமாகி முன்கூட்டியே காய்ந்துவிடும்.",
        "causes": "Alternaria solani fungus surviving in solanaceous crop residues.",
        "causes_ta": "அல்டர்னேரியா சோலானி பூஞ்சை.",
        "next_steps": "Avoid over-irrigation; maintain optimal plant vigor with balanced nitrogen; harvest in dry conditions.",
        "next_steps_ta": "அதிக பாசனத்தை தவிர்க்கவும்; சீரான தழைச்சத்து பராமரிக்கவும்.",
        "prevention": "Certified disease-free seed tubers; 3-year crop rotation.",
        "prevention_ta": "சான்றளிக்கப்பட்ட விதைக்கிழங்குகளை நடவு செய்யவும்; மாற்றுப்பயிர் சுழற்சி செய்யவும்.",
        "ipm": "Preventive sprays of Mancozeb 75% WP @ 2.5 g/L or Chlorothalonil.",
        "action_plan": {
            "urgency": "High — Action within 48 Hours",
            "urgency_ta": "அவசரம் — 48 மணி நேரத்திற்குள் நடவடிக்கை தேவை",
            "step_1_immediate": "Prune severely spotted lower leaves. Maintain hill soil cover around tubers.",
            "step_1_immediate_ta": "அதிகம் பாதிக்கப்பட்ட கீழ் இலைகளை அகற்றவும். கிழங்குகள் மீது மண் அணைக்கவும்.",
            "step_2_biological_cultural": "Top-dress with balanced potassium to fortify cell walls against fungal penetration.",
            "step_2_biological_cultural_ta": "சாம்பல் சத்து (பொட்டாஷ்) இட்டு பயிரின் நோய் எதிர்ப்பு திறனை அதிகரிக்கவும்.",
            "step_3_chemical_application": "Spray Chlorothalonil 75% WP @ 2.0 g/L water (400-500 g/acre) OR Mancozeb 75% WP @ 2.5 g/L.",
            "step_3_chemical_application_ta": "குளோரோதலோனில் (2.0 கிராம்/லிட்டர்) அல்லது மேன்கோசெப் (2.5 கிராம்/லிட்டர்) தெளிக்கவும்.",
            "step_4_monitoring": "Re-inspect lower leaves after 7 days.",
            "step_4_monitoring_ta": "7 நாட்களுக்கு பின் இலைகளை மீண்டும் கண்காணிக்கவும்.",
            "critical_donots": [
                "DO NOT let foliage stay wet overnight.",
                "DO NOT harvest during wet rains."
            ],
            "critical_donots_ta": [
                "இரவு நேரத்தில் இலைகளில் நீர் தேங்க விட வேண்டாம்.",
                "மழை பெய்யும் போது கிழங்குகளை அறுவடை செய்ய வேண்டாம்."
            ]
        }
    },
    "Potato___healthy": {
        "crop": "Potato",
        "crop_ta": "உருளைக்கிழங்கு",
        "disease": "Healthy Plant",
        "disease_ta": "ஆரோக்கியமான பயிர்",
        "disease_type": "healthy",
        "severity": "None",
        "is_healthy": True,
        "symptoms": "Uniform deep green foliage, robust stems, no leaf spotting, leaf roll, or blighting symptoms.",
        "symptoms_ta": "இலைகள் எவ்வித கருகல் அல்லது புள்ளிகள் இன்றி அடர்பச்சை நிறத்துடன் நலமாக உள்ளன.",
        "causes": "Good seed tuber quality, proper hilling, balanced fertilization.",
        "causes_ta": "தரமான விதைக்கிழங்கு மற்றும் நல்ல பராமரிப்பு.",
        "next_steps": "Ensure adequate earthing up to prevent tuber greening. Scout for aphid vectors.",
        "next_steps_ta": "மண் அணைத்தல் பணிகளை முறையாக செய்யவும்; அசுவினி பூச்சிகளை கண்காணிக்கவும்.",
        "prevention": "Consistent crop rotation and soil testing.",
        "prevention_ta": "மண் பரிசோதனை செய்து சத்துக்களை நிர்வகிக்கவும்.",
        "ipm": "Deploy yellow sticky traps for aphid monitoring.",
        "action_plan": {
            "urgency": "Routine — Keep Vigilant for Weather Spells",
            "urgency_ta": "வழக்கமான பராமரிப்பு — வானிலை மாற்றங்களை கவனிக்கவும்",
            "step_1_immediate": "No chemical application needed. Conduct routine earthing-up.",
            "step_1_immediate_ta": "மருந்து தேவையில்லை. மண் அணைத்தல் பணியை செய்யவும்.",
            "step_2_biological_cultural": "Keep yellow sticky traps (10/acre) to detect viral vector aphids early.",
            "step_2_biological_cultural_ta": "மஞ்சள் பொறிகளை வைத்து அசுவினி பூச்சிகளை கண்காணிக்கவும்.",
            "step_3_chemical_application": "Zero chemicals required.",
            "step_3_chemical_application_ta": "எந்த ரசாயன மருந்தும் தேவையில்லை.",
            "step_4_monitoring": "Weekly foliar inspection.",
            "step_4_monitoring_ta": "வாரம் ஒருமுறை கள ஆய்வு செய்யவும்.",
            "critical_donots": ["DO NOT apply fungicides without symptoms."],
            "critical_donots_ta": ["அறிகுறிகள் இன்றி மருந்துகளை தெளிக்க வேண்டாம்."]
        }
    },
    "Corn_(maize)___Common_rust_": {
        "crop": "Corn (Maize)",
        "crop_ta": "மக்காச்சோளம்",
        "disease": "Common Rust (Puccinia sorghi)",
        "disease_ta": "துரு நோய்",
        "disease_type": "fungal",
        "severity": "Moderate",
        "is_healthy": False,
        "symptoms": "Small, powdery, cinnamon-brown to dark reddish-brown pustules scattered across both upper and lower leaf surfaces.",
        "symptoms_ta": "இலையின் இரு புறங்களிலும் துரு போன்ற செம்பழுப்பு நிற சிறு கொப்புளங்கள் தோன்றும்.",
        "causes": "Puccinia sorghi fungal spores carried over long distances on wind currents.",
        "causes_ta": "பக்சீனியா சோர்கி பூஞ்சை.",
        "next_steps": "Assess disease severity. If pustules appear late in the season, chemical treatment is usually not economical.",
        "next_steps_ta": "பயிர் முதிர்ச்சி அடையும் தருவாயில் பாதிப்பு குறைந்திருந்தால் மருந்து தெளிப்பு தேவையில்லை.",
        "prevention": "Select resistant maize hybrids with Rp genetic resistance; early planting.",
        "prevention_ta": "துரு நோய் எதிர்ப்பு சக்தி கொண்ட கலப்பின விதைகளை தேர்வு செய்யவும்.",
        "ipm": "Foliar azoxystrobin or propiconazole fungicide only if >5% leaf area affected before silking.",
        "action_plan": {
            "urgency": "Moderate — Economic Threshold Evaluation",
            "urgency_ta": "மிதமான அவசரம் — பாதிப்பு வரம்பை கணக்கிட்டு நடவடிக்கை",
            "step_1_immediate": "Count pustules on the ear leaf. If <5% leaf area is affected, withhold spraying as economic injury level is not reached.",
            "step_1_immediate_ta": "கதிர் இலையில் துரு புள்ளிகளை எண்ணவும்; 5%க்கு குறைவாக இருந்தால் மருந்து தெளிக்க வேண்டாம்.",
            "step_2_biological_cultural": "Ensure proper field drainage and air passage between rows.",
            "step_2_biological_cultural_ta": "வரிசைகளுக்கிடையே போதிய காற்றோட்டம் கிடைக்கச் செய்யவும்.",
            "step_3_chemical_application": "If pustules exceed threshold before silking, spray Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1.0 ml/L water (200 ml/acre).",
            "step_3_chemical_application_ta": "கதிர் வரும் முன் பாதிப்பு தீவிரமானால் அஸோக்ஸிஸ்ட்ரோபின் + டைபனோகொனசோல் (1.0 மி.லி/லிட்டர்) தெளிக்கவும்.",
            "step_4_monitoring": "Re-evaluate at blister stage (R2).",
            "step_4_monitoring_ta": "தானிய பால் பிடிக்கும் தருவாயில் மீண்டும் சோதிக்கவும்.",
            "critical_donots": [
                "DO NOT spray fungicides after dough stage (R4) — economic return is negligible.",
                "DO NOT use insecticides for rust pustules."
            ],
            "critical_donots_ta": [
                "பயிர் முதிர்ந்த பின் மருந்து தெளிக்க வேண்டாம் — செலவு வீணாகும்.",
                "துரு நோய்க்கு பூச்சிக்கொல்லிகளை தெளிக்க வேண்டாம்."
            ]
        }
    },
    "Corn_(maize)___healthy": {
        "crop": "Corn (Maize)",
        "crop_ta": "மக்காச்சோளம்",
        "disease": "Healthy Plant",
        "disease_ta": "ஆரோக்கியமான பயிர்",
        "disease_type": "healthy",
        "severity": "None",
        "is_healthy": True,
        "symptoms": "Broad, vibrant green leaves with intact margins, strong stalk development, no fungal sporulation.",
        "symptoms_ta": "அகன்ற பசுமையான இலைகள், திடமான தண்டுடன் ஆரோக்கியமாக உள்ளது.",
        "causes": "Adequate nitrogen, timely weed management, optimal plant population.",
        "causes_ta": "சரியான பயிர் இடைவெளி மற்றும் சத்து மேலாண்மை.",
        "next_steps": "Scout for Fall Armyworm whorl damage; maintain irrigation during silking.",
        "next_steps_ta": "படைப்புழு தாக்குதல் உள்ளதா என தொடர்ந்து கண்காணிக்கவும்.",
        "prevention": "Pheromone traps for monitoring insect flights.",
        "prevention_ta": "இனக்கவர்ச்சி பொறிகளை அமைத்து பூச்சிகளை கண்காணிக்கவும்.",
        "ipm": "Conserve natural predators like earwigs and Trichogramma parasitoids.",
        "action_plan": {
            "urgency": "Routine — Monitor Silking and Grain Filling",
            "urgency_ta": "வழக்கமான பராமரிப்பு — கதிர் பிடிப்பை கண்காணிக்கவும்",
            "step_1_immediate": "Maintain irrigation during critical silking and tassel emergence.",
            "step_1_immediate_ta": "பூக்கும் மற்றும் கதிர் பிடிக்கும் தருவாயில் பாசனத்தை சீராக வைக்கவும்.",
            "step_2_biological_cultural": "Deploy Fall Armyworm pheromone traps (5/acre).",
            "step_2_biological_cultural_ta": "படைப்புழு இனக்கவர்ச்சி பொறிகளை வைக்கவும்.",
            "step_3_chemical_application": "Zero fungicides required.",
            "step_3_chemical_application_ta": "மருந்துகள் தேவையில்லை.",
            "step_4_monitoring": "Inspect whorls weekly.",
            "step_4_monitoring_ta": "வாரந்தோறும் குருத்துகளை கண்காணிக்கவும்.",
            "critical_donots": ["DO NOT allow water stress during silking."],
            "critical_donots_ta": ["கதிர் வரும் போது தண்ணீர் தட்டுப்பாடு ஏற்பட விட வேண்டாம்."]
        }
    }
}


def get_class_profile(class_name: str) -> Dict[str, Any]:
    """Retrieve full disease metadata profile or provide a structured fallback."""
    if class_name in DISEASE_PROFILES:
        return DISEASE_PROFILES[class_name]

    parts = class_name.split("___")
    crop = parts[0].replace("_", " ").replace("(", "").replace(")", "").strip()
    disease_raw = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown Condition"
    is_healthy = "healthy" in disease_raw.lower()

    disease_type = (
        "healthy" if is_healthy
        else ("fungal" if any(w in disease_raw.lower() for w in ["blight", "rot", "scab", "rust", "mildew", "spot", "scorch"])
        else "bacterial" if "bacteri" in disease_raw.lower()
        else "viral" if "virus" in disease_raw.lower()
        else "pest" if "mite" in disease_raw.lower()
        else "other")
    )

    return {
        "crop": crop,
        "crop_ta": crop,
        "disease": "Healthy Plant" if is_healthy else disease_raw,
        "disease_ta": "ஆரோக்கியமான பயிர்" if is_healthy else disease_raw,
        "disease_type": disease_type,
        "severity": "None" if is_healthy else "Moderate",
        "is_healthy": is_healthy,
        "symptoms": "No visible disease symptoms. Leaf foliage appears uniform and healthy." if is_healthy else f"Foliar lesions, discoloration, or spotting associated with {disease_raw}.",
        "symptoms_ta": "நோய் அறிகுறிகள் இன்றி ஆரோக்கியமாக உள்ளது." if is_healthy else f"{disease_raw} தொடர்பான இலைப்புள்ளி அல்லது நிறமாற்றம்.",
        "causes": "Optimal cultural conditions." if is_healthy else f"Pathogen or stress factor responsible for {disease_raw}.",
        "causes_ta": "முறையான பராமரிப்பு." if is_healthy else f"{disease_raw} காரணி.",
        "next_steps": "Continue routine field monitoring." if is_healthy else "Isolate affected specimens and consult local Krishi Vigyan Kendra.",
        "next_steps_ta": "தொடர்ந்து கண்காணிக்கவும்." if is_healthy else "வேளாண் நிபுணர்களை அணுகி ஆலோசனை பெறவும்.",
        "prevention": "Standard crop rotation and sanitation." if is_healthy else "Crop rotation and certified disease-free planting material.",
        "prevention_ta": "பயிர் சுழற்சி மற்றும் தூய்மை." if is_healthy else "சான்றளிக்கப்பட்ட விதைகளை உபயோகிக்கவும்.",
        "ipm": "Regular scouting and beneficial predator conservation." if is_healthy else "Monitor field threshold levels before chemical interventions.",
        "action_plan": {
            "urgency": "Standard Advisory" if is_healthy else "Moderate — Field Inspection Recommended",
            "urgency_ta": "வழக்கமான ஆலோசனை" if is_healthy else "மிதமான அவசரம் — கள ஆய்வு பரிந்துரைக்கப்படுகிறது",
            "step_1_immediate": "Inspect adjacent crop rows and remove suspicious dried or spotted leaf tissue.",
            "step_1_immediate_ta": "அருகிலுள்ள பயிர்களை ஆய்வு செய்து காய்ந்த இலைகளை அகற்றவும்.",
            "step_2_biological_cultural": "Enhance plant vigor through balanced organic compost and drip irrigation.",
            "step_2_biological_cultural_ta": "மக்கிய உரம் மற்றும் சொட்டு நீர் பாசனம் மூலம் பயிரை வலுப்படுத்தவும்.",
            "step_3_chemical_application": "Consult nearest Krishi Vigyan Kendra (KVK) for certified local registration before chemical purchase.",
            "step_3_chemical_application_ta": "மருந்து வாங்குவதற்கு முன் அருகிலுள்ள KVK அலுவலரை அணுகவும்.",
            "step_4_monitoring": "Repeat observation in 5 to 7 days.",
            "step_4_monitoring_ta": "5 முதல் 7 நாட்களில் மீண்டும் கண்காணிக்கவும்.",
            "critical_donots": [
                "DO NOT spray random chemical mixtures without verified pest diagnosis.",
                "DO NOT exceed manufacturer label concentration rates."
            ],
            "critical_donots_ta": [
                "காரணம் அறியாமல் கண்ட மருந்துகளை கலந்து தெளிக்க வேண்டாம்.",
                "அளவுக்கதிகமான செறிவில் மருந்துகளை உபயோகிக்க வேண்டாம்."
            ]
        }
    }
