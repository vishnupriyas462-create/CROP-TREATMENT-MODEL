# AgriGuard AI — Smart Crop Health Assistant 🌾

An AI-powered agricultural decision-support web application that detects crop diseases from leaf photographs, provides evidence-based pathological explanations in English and Tamil, and delivers verified pesticide, fungicide, and Integrated Pest Management (IPM) recommendations strictly cited from accredited agricultural institutions (ICAR, DPPQS, and TNAU).

---

## 🌟 Key Features

1. **Computer Vision Leaf Disease Classification**:
   - Transfer learning architecture using **PyTorch MobileNetV2**.
   - 38 multi-crop disease classes covering **Tomato, Potato, Corn (Maize), Bell Pepper, Rice, Cotton, Apple, Grape, Strawberry, Peach, Cherry, Squash, and Soybean**.
   - Built-in OpenCV HSV foliar heuristic filter to reject unsuitable non-plant images (e.g., vehicles, synthetic objects).

2. **Responsible, Evidence-Based Treatment Guidance**:
   - Zero hallucinated chemicals: Recommendations are strictly queried from an authoritative database verified against **ICAR (Indian Council of Agricultural Research)**, **DPPQS (Directorate of Plant Protection, Quarantine & Storage)**, and **TNAU (Tamil Nadu Agricultural University)** protocols.
   - **Pathogen-Treatment Type Matching**: Insecticides are never recommended for fungal infections. Fungicides are not misprescribed for bacterial spots.
   - Complete package details: Approved active ingredients, commercial formulations, dosage guidance, non-chemical & biological alternatives, personal protective equipment (PPE), and Pre-Harvest Intervals (PHI).

3. **Bilingual User Experience (English & Tamil / தமிழ்)**:
   - Instant language toggle for navigation, field instructions, disease descriptions, causal factors, and safety precautions.

4. **Statistical Confidence & Uncertainty Safeguards**:
   - Displays prediction confidence percentage alongside confidence rating (High / Moderate / Low).
   - Configurable uncertainty threshold (default 60%). If confidence falls below 60%, the system displays a prominent advisory warning: *"Uncertain prediction — upload a clearer image or consult an agricultural expert."*

5. **Historical Analysis & PDF Diagnostic Reports**:
   - Persistent SQLite archive with search, filtering by crop and health status.
   - One-click server-generated printable PDF diagnostic report (ReportLab engine).
   - Record deletion and diagnostic validation feedback submission.

6. **Official Agricultural Helpline Directory**:
   - Direct contact links for the **Kisan Call Center (Toll-Free 1800-180-1551)**, TNAU Agritech Center, and National KVK Portal.

---

## 🏗️ Project Architecture

```
cdis/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI entry point & lifespan events
│   │   ├── config.py              # Environment configuration & pydantic settings
│   │   ├── database.py            # SQLite database engine & schema creation
│   │   ├── schemas.py             # Pydantic v2 schemas for request/response
│   │   ├── data/
│   │   │   └── seed_data.py       # Seed data for crops, verified guidance & helplines
│   │   ├── ml/
│   │   │   ├── model.py           # PyTorch MobileNetV2 architecture
│   │   │   ├── classes.py         # 38 PlantVillage classes & bilingual profiles
│   │   │   ├── inference.py       # Image preprocessing & forward-pass inference
│   │   │   ├── train.py           # Training pipeline with data augmentation
│   │   │   └── evaluate.py        # Evaluation metrics & confusion matrix
│   │   ├── routers/
│   │   │   ├── health.py          # GET /api/health
│   │   │   ├── crops.py           # GET /api/crops, GET /api/diseases, GET /api/advisory-contacts
│   │   │   ├── predict.py         # POST /api/predict (leaf image analysis)
│   │   │   ├── history.py         # GET/DELETE /api/history & PDF export
│   │   │   ├── recommendations.py # GET /api/recommendations (searchable KB)
│   │   │   ├── feedback.py        # POST /api/feedback
│   │   │   └── analytics.py       # GET /api/analytics
│   │   └── services/
│   │       ├── knowledge_base.py  # Pathogen-verified guidance query service
│   │       └── pdf_service.py     # ReportLab PDF report generation
│   ├── ml_weights/
│   │   ├── mobilenetv2_plantvillage.pth # Runnable PyTorch model checkpoint (10MB)
│   │   └── generate_baseline_weights.py # Weights generator
│   ├── tests/
│   │   ├── test_api.py            # Automated pytest test suite
│   │   └── create_sample_images.py# Test image fixtures generator
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/            # Navbar, Footer, ImageUpload, TreatmentCard, StatCard, etc.
│   │   ├── pages/                 # Landing, Dashboard, Analyze, Result, Treatments, Library, History, Advisory
│   │   ├── i18n/                  # English & Tamil translations and context
│   │   ├── services/api.ts        # Client API service
│   │   ├── types/index.ts         # TypeScript interfaces
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── vercel.json                # Vercel deployment SPA rewrite configuration
│   └── .env.example
├── render.yaml                    # Render Web Service blueprint
└── README.md
```

---

## 🚀 Quickstart Local Execution

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Node.js 18+ and npm

### 1. Backend Setup

```bash
cd backend

# Create and activate a virtual environment (optional)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Verify PyTorch model weights exist
python -m ml_weights.generate_baseline_weights

# Run the automated backend test suite
python -m pytest -v tests/test_api.py

# Start the FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The interactive FastAPI Swagger documentation will be accessible at:
👉 **`http://localhost:8000/docs`**

### 2. Frontend Setup

In a separate terminal:

```bash
cd frontend

# Install npm dependencies
npm install

# Start Vite development server
npm run dev
```

Open your browser at:
👉 **`http://localhost:5173`**

---

## 📡 REST API Specifications

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Backend and database health status |
| `GET` | `/api/crops` | List of supported crop profiles |
| `GET` | `/api/diseases` | Detailed catalogue of supported diseases |
| `POST` | `/api/predict` | Upload leaf image (JPEG, PNG, WebP) for ML diagnosis |
| `GET` | `/api/history` | Retrieve previous crop scan records (filterable) |
| `GET` | `/api/history/{id}` | Retrieve individual diagnostic report |
| `DELETE` | `/api/history/{id}` | Delete a diagnostic report |
| `GET` | `/api/history/{id}/pdf` | Download official diagnostic report as PDF |
| `GET` | `/api/recommendations` | Search verified agricultural guidance & IPM |
| `POST` | `/api/feedback` | Submit farmer/expert diagnostic feedback |
| `GET` | `/api/analytics` | Live dashboard metrics and distributions |
| `GET` | `/api/advisory-contacts` | Official agricultural helpline numbers and KVKs |

---

## 🧠 Machine Learning Details & Dataset

### Dataset: PlantVillage
- Based on the standard **PlantVillage** dataset (Mohanty et al.):
  [https://huggingface.co/datasets/mohanty/PlantVillage](https://huggingface.co/datasets/mohanty/PlantVillage)
- Multi-crop distribution across 38 classes.

### Training Pipeline (`backend/app/ml/train.py`)
- **Base Architecture**: MobileNetV2 with transfer learning (ImageNet pre-trained feature extractor).
- **Custom Classifier**: Dropout(0.3) -> Linear(1280, 256) -> ReLU -> Dropout(0.2) -> Linear(256, 38).
- **Data Augmentation**: RandomResizedCrop(224), RandomHorizontalFlip, RandomVerticalFlip, RandomRotation(15°), ColorJitter.
- **Normalization**: ImageNet mean `[0.485, 0.456, 0.406]` and std `[0.229, 0.224, 0.225]`.
- **Optimizer & Scheduler**: AdamW with Cosine Annealing learning rate schedule.
- **Evaluation Metrics**: Evaluated via Accuracy, Precision, Recall, Macro/Weighted F1-score, and Confusion Matrix.

### Foliar Heuristic Filter (`backend/app/ml/inference.py`)
To prevent non-agricultural photographs (such as automobiles, human faces, or random textures) from receiving arbitrary disease classifications, an OpenCV HSV color filter evaluates the foliar vegetation ratio (green, yellow, and necrotic brown tones). If foliar coverage is under 15%, the system safely rejects the upload with an informative message.

---

## 🌐 Production Deployment Guide

### Frontend Deployment (Vercel)

1. Push your repository to GitHub.
2. Log in to [Vercel](https://vercel.com) and click **"Add New Project"**.
3. Select the repository and configure the Root Directory as `frontend`.
4. Build Settings:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Environment Variables:
   ```env
   VITE_API_BASE_URL=https://your-backend-app.onrender.com
   ```
6. Deploy. The `frontend/vercel.json` file ensures client-side SPA routing rewrites work properly.

### Backend Deployment (Render)

1. Log in to [Render](https://render.com) and click **"New Web Service"**.
2. Connect your GitHub repository.
3. Configure the service:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/api/health`
4. Environment Variables:
   ```env
   ENVIRONMENT=production
   PORT=10000
   MODEL_PATH=./ml_weights/mobilenetv2_plantvillage.pth
   CONFIDENCE_THRESHOLD=0.60
   CORS_ORIGINS=https://your-frontend-app.vercel.app,http://localhost:5173
   ENABLE_IMAGE_STORAGE=true
   UPLOAD_DIR=./uploads
   ```
5. Deploy. You can also use the included `render.yaml` for one-click blueprint setup.

---

## 🛡️ Agricultural Safety & Statutory Disclaimer

> **Important Agricultural Notice:**
> AgriGuard AI is an automated educational decision-support tool. Machine learning confidence scores reflect mathematical visual pattern similarity, **not** a certified phytopathological laboratory diagnosis.
> 
> - **Never** apply synthetic chemical pesticides or fungicides without reading and adhering to the manufacturer's registered product label.
> - **Never** mix unauthorized chemical combinations or exceed prescribed application doses.
> - Always wear personal protective equipment (PPE) and observe Pre-Harvest Intervals (PHI).
> - For severe pest infestations or sudden crop failure, contact your local **Krishi Vigyan Kendra (KVK)** or dial the **National Kisan Call Center at 1800-180-1551**.

---

## 📄 License
This project is released under the **MIT License**.
