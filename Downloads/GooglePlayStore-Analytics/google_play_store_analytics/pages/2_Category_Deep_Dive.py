"""
Category Deep Dive Analytics Page.

Provides detailed drill-down into specific product categories, displaying
correlation scatters, price distributions, and developer design benchmarks.
"""

import streamlit as st
import plotly.express as px
from utils.styles import inject_custom_css, render_insight_card
from core.analytics import generate_benchmark_insights


def main():
    inject_custom_css()

    st.markdown("## 🎯 Category Drilldown & Benchmarking")
    st.write(
        "Conduct rigorous deep dives into specific market verticals. This module identifies size "
        "footprints, premium price tolerances, and generates specific developer release suggestions."
    )

    if "raw_data" not in st.session_state:
        st.warning("Please run the main landing page (app.py) first to initialize data.")
        st.stop()

    df = st.session_state["raw_data"]

    # Sidebar category selection
    all_categories = sorted(df["Category"].unique().tolist())
    st.sidebar.markdown('<div class="sidebar-header">🎯 Category Drilldown</div>', unsafe_allow_html=True)
    selected_category = st.sidebar.selectbox(
        "Select Target Category",
        options=all_categories,
        index=0,
        help="Select a specific vertical to generate design benchmarks and distributions"
    )

    # Filter data for the single category
    cat_df = df[df["Category"] == selected_category]

    if cat_df.empty:
        st.warning(f"No records available for category: {selected_category}")
        st.stop()

    # Calculate dynamic benchmarks
    benchmarks = generate_benchmark_insights(df, selected_category)

    # 1. Benchmarks Grid layout
    st.markdown(f"### 📋 '{selected_category}' Developer Release Benchmarks")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.metric(
            label="Ideal File Footprint",
            value=f"{benchmarks['ideal_size_range_mb'][0]} - {benchmarks['ideal_size_range_mb'][1]} MB",
            help="Optimal file sizing based on top-quartile ratings (Rating >= 4.4)"
        )
    with col_b2:
        st.metric(
            label="Optimal Premium Price Point",
            value=f"${benchmarks['suggested_price']}",
            help="Suggested listing retail price derived from successful paid competitors"
        )
    with col_b3:
        st.metric(
            label="Target Audience Optimization",
            value=benchmarks["recommended_target_audience"],
            help="Most common age-tier constraint among top-performing apps"
        )

    st.markdown(render_insight_card("Strategic Action Recommendation", benchmarks["recommendation"]), unsafe_allow_html=True)

    st.markdown("---")

    # 2. Page Visualizations Section (3 Charts on this page)
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("### 🔬 App Size vs. Rating Correlation")
        # Visual 4: Scatter Plot with bubble sizing representing Installs
        fig_scatter = px.scatter(
            cat_df,
            x="Size_MB",
            y="Rating",
            size="Installs_Numeric",
            hover_name="App",
            color="Type",
            labels={"Size_MB": "File Size (MB)", "Rating": "App Rating", "Installs_Numeric": "Downloads"},
            color_discrete_map={"Free": "#3B82F6", "Paid": "#EF4444"},
            size_max=35
        )
        fig_scatter.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_chart2:
        st.markdown("### 💵 Pricing Elasticity Distribution")
        # Visual 5: Price distribution histogram or box plot (Paid apps only if possible)
        paid_df = cat_df[cat_df["Type"] == "Paid"]
        if paid_df.empty:
            st.info("There are no Paid apps in this category to show pricing distribution. All offerings are Free.")
            # Show fallback content rating donut chart
            fig_fallback = px.pie(
                cat_df,
                names="Content Rating",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_fallback.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=380, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_fallback, use_container_width=True)
        else:
            fig_box = px.box(
                paid_df,
                y="Price_Numeric",
                points="all",
                hover_data=["App"],
                labels={"Price_Numeric": "Listing Price ($)"},
                color_discrete_sequence=["#F59E0B"]
            )
            fig_box.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                height=380,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    col_bottom = st.columns([12, 8])
    with col_bottom[0]:
        st.markdown("### 🎯 Audience Age Segments Market Share")
        # Visual 6: Age rating distribution for category
        age_counts = cat_df["Content Rating"].value_counts().reset_index()
        age_counts.columns = ["Audience", "App Count"]
        
        fig_age = px.bar(
            age_counts,
            x="Audience",
            y="App Count",
            color="Audience",
            color_discrete_sequence=px.colors.qualitative.Set2,
            text="App Count"
        )
        fig_age.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with col_bottom[1]:
        st.markdown("### 📊 Segment Vital Signs")
        st.write(
            f"Analyzing the **{len(cat_df)}** apps mapped to **{selected_category}** reveals:"
        )
        st.write(f"- **Monetization Structure**: {benchmarks['monetization_viability']}.")
        st.write(f"- **User Favorability Index**: Score of **{benchmarks['general_sentiment_index']}** ({benchmarks['sentiment_label']}).")
        st.write(f"- **Total Market Scale**: Average rating of **{cat_df['Rating'].mean():.2f}**/5.0, with average downloads reaching **{cat_df['Installs_Numeric'].mean():,.0f}** per app.")


if __name__ == "__main__":
    main()
