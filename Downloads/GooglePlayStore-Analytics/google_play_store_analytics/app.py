"""
Main Streamlit Application Entrypoint.

Handles application configuration, global session state initialization, data loading,
and displays the primary Portfolio Landing Page detailing the enterprise-level
software architecture of the platform.
"""

import os
import streamlit as st

# 1. Page Configuration (Must be first Streamlit call)
st.set_page_config(
    page_title="Google Play Store Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import Custom CSS and Core Modules
from utils.styles import inject_custom_css, render_insight_card
from core.data_loader import load_and_preprocess_data


def main():
    # Inject Custom responsive CSS styling
    inject_custom_css()

    # Title & Corporate Header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 30px;">
            <p style="color: #3B82F6; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 5px;">Recruiter & Portfolio Showcase</p>
            <h1 style="font-size: 3rem; margin-top: 0; margin-bottom: 10px;">Google Play Store Analytics Platform</h1>
            <p style="color: #64748B; font-size: 1.15rem; max-width: 800px; margin: 0 auto; line-height: 1.6;">
                A production-ready data science web application demonstrating enterprise-tier architecture,
                predictive data pipelines, interactive business intelligence, and user sentiment analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Session State Initialization
    if "raw_data" not in st.session_state:
        # Resolve data path dynamically
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "data", "raw", "googleplaystore.csv")
        
        try:
            with st.spinner("Initializing Preprocessing Data Engine..."):
                st.session_state["raw_data"] = load_and_preprocess_data(data_path)
            st.toast("✅ Google Play Store dataset loaded & preprocessed successfully!", icon="🚀")
        except Exception as e:
            st.error(f"Critical error initializing data engine: {e}")
            st.stop()

    df = st.session_state["raw_data"]

    # 3. Main Dashboard Layout - Two Columns (Portfolio Pitch & Architectural Design)
    col_pitch, col_arch = st.columns([11, 9], gap="large")

    with col_pitch:
        st.markdown("### 🏆 Portfolio & Internship Highlights")
        st.write(
            """
            This platform acts as an end-to-end recruiter demonstration, showcasing a modern, robust, 
            and scalable approach to building analytical tools in Python.
            
            **Highlights for Recruiters & Engineering Leads:**
            - **Robust Data Pipeline**: Secure loader with Regex cleaning, type casing, and category-level statistical median imputation.
            - **Multipage Navigation**: Clean architectural division across executive, category, sentiment, and explorer views.
            - **Interactive Visualizations**: 10+ Plotly-powered interactive charts covering distribution, correlation, and growth curves.
            - **Business Insight Engine**: Contextual recommendations generated dynamically based on active filters and historical market thresholds.
            - **Enterprise Code Standards**: Fully compliant with PEP 8, structured with static type hints, robust logger coverage, and full docstrings.
            """
        )

        st.markdown(
            render_insight_card(
                "Executive Perspective",
                "Data is only as valuable as the decisions it empowers. Rather than just plotting counts, "
                "this dashboard calculates business viability benchmarks, target audience optimizations, "
                "and consumer sentiment profiles to help developers maximize launch success."
            ),
            unsafe_allow_html=True
        )
        
        # Display Brief Data Overview
        st.markdown("#### 🔍 Dataset At A Glance")
        st.dataframe(
            df[["App", "Category", "Rating", "Reviews", "Installs", "Type", "Price", "Content Rating"]]
            .head(5),
            use_container_width=True
        )

    with col_arch:
        st.markdown("### 🏗️ Platform Software Architecture")
        st.markdown(
            """
            ```text
            ┌─────────────────────────────────────────────────────────┐
            │                     Presentation Layer                  │
            │        Streamlit UI / KPI Cards / Responsive Canvas     │
            └────────────────────────────┬────────────────────────────┘
                                         ▼
            ┌─────────────────────────────────────────────────────────┐
            │                     Application Layer                   │
            │       Routing / Global Search Filters / Session State   │
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
            """
        )
        
        with st.expander("📂 View Complete Directory Blueprint"):
            st.markdown(
                """
                ```text
                GooglePlayStore-Analytics/
                ├── app.py                     # Primary Routing & Landing
                ├── requirements.txt           # Dependencies Config
                ├── config/                    # Environment & Theme Settings
                ├── data/
                │   ├── raw/
                │   │   └── googleplaystore.csv # Raw Dataset
                │   └── exports/               # Dynamic User Reports
                ├── core/
                │   ├── data_loader.py         # Cleaning & Preprocessing
                │   └── analytics.py           # Metrics & Statistics
                ├── utils/
                │   └── styles.py              # Custom CSS Injector
                └── pages/
                    ├── 1_Executive_Summary.py # Strategic KPI Dashboard
                    ├── 2_Category_Deep_Dive.py# Segment Analysis
                    ├── 3_Sentiment_Analysis.py# Qualitative Analysis
                    └── 4_Interactive_Explorer.# User Drilldown Engine
                ```
                """
            )

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 15px 0;">
            Google Play Store Data Analytics Platform • Built with Python, Streamlit, and Plotly.
            Use the sidebar navigation to explore the different analysis views.
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
