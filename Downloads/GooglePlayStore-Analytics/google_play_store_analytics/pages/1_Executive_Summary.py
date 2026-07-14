"""
Executive Summary Analytics Page.

Displays high-level corporate metrics, market ratios, and category performance
with automated business insights.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import inject_custom_css, render_styled_kpi, render_insight_card
from core.analytics import get_kpi_metrics, calculate_category_summaries


def render_sidebar_filters(df):
    """Render unified sidebar filters and return filtered dataframe."""
    st.sidebar.markdown('<div class="sidebar-header">🎛️ Control Panel</div>', unsafe_allow_html=True)
    
    # Category search
    all_categories = sorted(df["Category"].unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=all_categories,
        default=all_categories[:5], # Default select first 5
        help="Filter dashboard metrics by specific app categories"
    )
    if not selected_categories:
        selected_categories = all_categories

    # App Type
    selected_type = st.sidebar.radio(
        "Distribution Type",
        options=["All", "Free", "Paid"],
        index=0,
        help="Select pricing model"
    )

    # Ratings filter
    min_rating, max_rating = st.sidebar.slider(
        "App Rating Range",
        min_value=1.0,
        max_value=5.0,
        value=(1.0, 5.0),
        step=0.1
    )

    # Filter operations
    filtered_df = df[
        (df["Category"].isin(selected_categories)) &
        (df["Rating"] >= min_rating) &
        (df["Rating"] <= max_rating)
    ]

    if selected_type != "All":
        filtered_df = filtered_df[filtered_df["Type"] == selected_type]

    return filtered_df, selected_categories


def main():
    inject_custom_css()

    st.markdown("## 📊 Executive Strategic Summary")
    st.write(
        "A high-level business intelligence view highlighting download volumes, market splits, "
        "and distribution channels. Use the controls in the sidebar to drill down."
    )

    if "raw_data" not in st.session_state:
        st.warning("Please run the main landing page (app.py) first to initialize data.")
        st.stop()

    df = st.session_state["raw_data"]
    
    # 1. Apply Filters
    filtered_df, selected_categories = render_sidebar_filters(df)

    if filtered_df.empty:
        st.error("No data matches current filter settings. Reset filters in the sidebar.")
        st.stop()

    # 2. Get Statistics
    kpi = get_kpi_metrics(filtered_df)

    # 3. Render KPI Grid (Power BI Style Cards)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            render_styled_kpi("Portfolio App Coverage", f"{kpi['total_apps']:,}", "Apps In Scope", True),
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            render_styled_kpi("Average App Rating", f"{kpi['avg_rating']}/5.0", f"Mean Platform Quality", True),
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            render_styled_kpi("Total Download Volume", f"{kpi['total_installs']:,}", "Gross Installs", True),
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            render_styled_kpi("User Favorable Ratio", f"{kpi['positive_sentiment_percent']}%", "Positive Sentiment", True),
            unsafe_allow_html=True
        )

    st.markdown("---")

    # 4. Data Visualizations Section (3 Charts on this page)
    col_left, col_right = st.columns([11, 9])

    # Category summary aggregates
    cat_summary = calculate_category_summaries(filtered_df)

    with col_left:
        st.markdown("### 📈 Download Volume Market Share by Category")
        # Visual 1: Horizontal Bar Chart of Installs by Category
        fig_installs = px.bar(
            cat_summary.sort_values(by="Total_Installs", ascending=True),
            x="Total_Installs",
            y="Category",
            orientation="h",
            labels={"Total_Installs": "Gross Installs", "Category": "Category"},
            color="Total_Installs",
            color_continuous_scale="blues",
            text="Total_Installs"
        )
        fig_installs.update_traces(texttemplate="%{text:.2s}", textposition="outside")
        fig_installs.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_installs, use_container_width=True)

    with col_right:
        st.markdown("### 🍩 Distribution Model Share")
        # Visual 2: Donut/Pie Chart of Free vs Paid
        type_counts = filtered_df["Type"].value_counts().reset_index()
        type_counts.columns = ["Model", "Count"]
        
        fig_pie = px.pie(
            type_counts,
            values="Count",
            names="Model",
            hole=0.4,
            color="Model",
            color_discrete_map={"Free": "#3B82F6", "Paid": "#F59E0B"}
        )
        fig_pie.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    col_bot_l, col_bot_r = st.columns([10, 10])

    with col_bot_l:
        st.markdown("### ⭐ Category Rating Quality Benchmarks")
        # Visual 3: Average Rating by Category
        fig_rating = px.bar(
            cat_summary.sort_values(by="Avg_Rating", ascending=False),
            x="Category",
            y="Avg_Rating",
            color="Avg_Rating",
            color_continuous_scale="greens",
            labels={"Avg_Rating": "Avg Rating"},
            text="Avg_Rating"
        )
        fig_rating.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_rating, use_container_width=True)

    with col_bot_r:
        st.markdown("### 📋 Executive Business Insights")
        # Generate insight report dynamically
        lead_category = cat_summary.iloc[0]["Category"] if not cat_summary.empty else "N/A"
        market_share = cat_summary.iloc[0]["Install_Market_Share_Percent"] if not cat_summary.empty else 0.0
        
        insight_text = (
            f"Based on active filters, **{lead_category}** represents the dominant market sector "
            f"with a **{market_share}%** download share. Free models continue to lead distribution, "
            f"accounting for **{kpi['free_ratio_percent']}%** of active offerings. Developers should note that "
            f"while download volumes cluster in communication and games, high quality ratings are distributed "
            f"broadly across niche utility modules. A launch strategy should optimize for an MVP entry "
            f"to test user receptiveness, securing early rating reviews to anchor platform recommendations."
        )
        st.markdown(render_insight_card("Strategic Performance Summary", insight_text), unsafe_allow_html=True)
        st.markdown(
            """
            **Key Actions Recommended:**
            1. **Verify Onboarding Performance**: Sentiment audits indicate early rating preservation is critical.
            2. **Freemium Pipeline Setup**: Due to high free dominance, premium pricing must be backed by heavy utility metrics.
            3. **Cross-Channel Marketing**: Coordinate launches around peak update periods (historically June-July).
            """
        )


if __name__ == "__main__":
    main()
