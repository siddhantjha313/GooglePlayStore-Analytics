"""
Custom CSS styling and injection utilities.

Enables elegant layouts, stylized KPI cards, custom sidebars, and custom fonts
to provide a modern, Power BI-inspired UX in Streamlit.
"""

import streamlit as st


def inject_custom_css() -> None:
    """Inject custom responsive styles into the active Streamlit runtime."""
    st.markdown(
        """
        <style>
        /* Import Elegant Display and Body Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

        /* Establish Corporate Palette and Typography */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            color: #1E293B; /* Slate 800 */
        }

        /* Power BI Styled Grid Metrics Container */
        .kpi-container {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            text-align: center;
        }

        .kpi-container:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
            border-color: #3B82F6; /* Accent color: Indigo Blue */
        }

        .kpi-title {
            font-size: 0.875rem;
            text-transform: uppercase;
            font-weight: 600;
            color: #64748B; /* Slate 500 */
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        }

        .kpi-value {
            font-size: 2rem;
            font-weight: 700;
            color: #0F172A; /* Slate 900 */
            font-family: 'Space Grotesk', sans-serif;
            margin-bottom: 4px;
        }

        .kpi-subtitle {
            font-size: 0.75rem;
            font-weight: 500;
            color: #10B981; /* Emerald 500 */
        }
        
        /* Sidebar styling additions */
        .sidebar-header {
            font-size: 1.25rem;
            font-weight: 700;
            color: #1E293B;
            margin-bottom: 20px;
            text-align: center;
            border-bottom: 2px solid #F1F5F9;
            padding-bottom: 12px;
        }
        
        /* Modern Info Alert and Callout Boxes */
        .insight-card {
            background-color: #F8FAFC;
            border-left: 5px solid #3B82F6;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }
        
        .insight-card h4 {
            margin-top: 0;
            color: #1E293B;
            font-weight: 600;
        }
        
        .insight-card p {
            color: #475569;
            font-size: 0.95rem;
            line-height: 1.5;
            margin-bottom: 0;
        }

        /* Customize Table Views */
        .dataframe {
            border: 1px solid #E2E8F0 !important;
            border-radius: 8px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_styled_kpi(title: str, value: str, subtitle: str = "", delta_positive: bool = True) -> str:
    """Return HTML string for standard Power BI-style KPI card to be rendered in markdown."""
    delta_color = "#10B981" if delta_positive else "#EF4444"
    return f"""
    <div class="kpi-container">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtitle" style="color: {delta_color};">{subtitle}</div>
    </div>
    """


def render_insight_card(title: str, text: str) -> str:
    """Return HTML string for elegant business insight summary card."""
    return f"""
    <div class="insight-card">
        <h4>💡 {title}</h4>
        <p>{text}</p>
    </div>
    """
