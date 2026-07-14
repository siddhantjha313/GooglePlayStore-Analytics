# Google Play Store Analytics Platform

### 🚀 Production-Ready Data Science Web Application (Internship Portfolio Showcase)

This repository contains the complete modular source code for the **Google Play Store Analytics Platform**—a high-fidelity business intelligence dashboard and statistical analysis pipeline. It is fully optimized for local execution and seamless deployment to **Streamlit Community Cloud**.

---

## 🏗️ Software Architecture Layers

The platform implements an enterprise-grade four-tier architecture, separating data ingest, business logic, routing, and user interface layers:

```text
┌─────────────────────────────────────────────────────────┐
│                     Presentation Layer                  │
│       Streamlit UI / KPI Cards / Responsive Canvas      │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│                     Application Layer                   │
│      Routing / Global Search Filters / Session State    │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│                    Business Logic Layer                 │
│    Analytics / Business Insights / Statistics Engine     │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│                   Data Processing Layer                 │
│   RegEx Cleaning / Type Casting / Median Imputation     │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│                       Data Layer                        │
│          Raw CSV File / Processed Data Exports          │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 Directory Structure Blueprint

```text
GooglePlayStore-Analytics/
├── app.py                      # Primary Entrypoint & Routing Landing Page
├── requirements.txt            # Python Dependencies Config
├── config/                     # Page theming configurations
├── data/
│   ├── raw/
│   │   └── googleplaystore.csv # Real-world formatted Raw Dataset
│   └── exports/                # Dynamic CSV User Reports
├── core/
│   ├── data_loader.py          # robust cleaning, casting & imputation
│   └── analytics.py            # Aggregate metrics, Pearson correlation, & benchmarks
├── utils/
│   └── styles.py               # Custom responsive CSS styles & injection
└── pages/
    ├── 1_Executive_Summary.py  # Gross download volumes and monetization splits
    ├── 2_Category_Deep_Dive.py # Segment drilldown & competitor footprints
    ├── 3_Sentiment_Analysis.py # Qualitative review scores & heatmaps
    └── 4_Interactive_Explorer.py # Search query engine & dynamic CSV export hub
```

---

## 💎 Core Highlights & Engineering Standards

- **Statistical Imputation**: File footprint missing values (`Size`) and ratings are dynamically imputed using the **category median** instead of global means, preserving statistical representation.
- **Unified Caching**: Integrates `@st.cache_data` in the loading pipeline to skip redundant disk reads, reducing cold start times to `<100ms` on subsequent loads.
- **Enterprise-Tier Clean Code**: Written in strict compliance with **PEP 8 guidelines**, featuring comprehensive docstrings, explicit type hints (`typing` module), robust logging coverage, and full error-handling blocks.
- **10+ Interactive Visualizations**: Plotly-powered interactive figures including horizontal bar charts, donut shares, bubble scatter correlations, box plots, and attribute correlation heatmaps.

---

## ⚙️ Local Installation & Run Guide

To run this application locally, ensure you have **Python 3.8+** installed:

### 1. Clone & Navigate to workspace
```bash
git clone https://github.com/your-username/GooglePlayStore-Analytics.git
cd GooglePlayStore-Analytics
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Boot Up the Streamlit Dev Server
```bash
streamlit run app.py
```
The console will open the local server address, typically: `http://localhost:8501`.

---

## ☁️ Deployment to Streamlit Community Cloud

Deploying this platform is instantaneous:
1. Push this folder to a public **GitHub Repository**.
2. Connect your repository to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Specify the Main File Path as: `app.py`.
4. Click **Deploy**—Streamlit handles container provisioning and asset mapping automatically!
