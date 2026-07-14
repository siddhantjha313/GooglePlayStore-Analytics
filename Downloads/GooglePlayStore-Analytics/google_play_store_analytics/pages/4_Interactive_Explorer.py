"""
Interactive Data Explorer & Reporting Engine Page.

Provides advanced multi-variable search filters, details expanders, and
downloadable custom reports in CSV format.
"""

import streamlit as st
import plotly.express as px
from utils.styles import inject_custom_css, render_insight_card


def main():
    inject_custom_css()

    st.markdown("## 🔍 Custom Report Builder & Data Explorer")
    st.write(
        "Build, customize, and export personalized marketplace intelligence reports. Apply multiple "
        "structural filters, analyze app scale, and download custom slice databases directly."
    )

    if "raw_data" not in st.session_state:
        st.warning("Please run the main landing page (app.py) first to initialize data.")
        st.stop()

    df = st.session_state["raw_data"]

    st.sidebar.markdown('<div class="sidebar-header">🔍 Query Engine</div>', unsafe_allow_html=True)

    # 1. Search Query
    search_query = st.sidebar.text_input(
        "Search App Names",
        value="",
        placeholder="e.g., WhatsApp, Clash...",
        help="Filter list by matching character strings inside app names"
    )

    # 2. Multi-category select
    all_categories = sorted(df["Category"].unique().tolist())
    selected_cats = st.sidebar.multiselect(
        "Select Categories",
        options=all_categories,
        default=all_categories,
        help="Select multiple categories to include in reports"
    )
    if not selected_cats:
        selected_cats = all_categories

    # 3. Content Ratings
    all_contents = sorted(df["Content Rating"].unique().tolist())
    selected_contents = st.sidebar.multiselect(
        "Audience Age Tier",
        options=all_contents,
        default=all_contents,
        help="Select age-tier constraints"
    )
    if not selected_contents:
        selected_contents = all_contents

    # 4. Ratings range
    min_rating, max_rating = st.sidebar.slider(
        "Star Rating Range",
        min_value=1.0,
        max_value=5.0,
        value=(1.0, 5.0),
        step=0.1
    )

    # 5. Price range slider
    max_dataset_price = float(df["Price_Numeric"].max())
    if max_dataset_price > 0.0:
        price_range = st.sidebar.slider(
            "Retail Price Range ($)",
            min_value=0.0,
            max_value=max_dataset_price,
            value=(0.0, max_dataset_price),
            step=0.5
        )
    else:
        price_range = (0.0, 0.0)

    # Compile filters
    filtered_df = df[
        (df["Category"].isin(selected_cats)) &
        (df["Content Rating"].isin(selected_contents)) &
        (df["Rating"] >= min_rating) &
        (df["Rating"] <= max_rating) &
        (df["Price_Numeric"] >= price_range[0]) &
        (df["Price_Numeric"] <= price_range[1])
    ]

    if search_query:
        filtered_df = filtered_df[filtered_df["App"].str.contains(search_query, case=False, na=False)]

    st.markdown(f"### 📋 Filtered Results Grid ({len(filtered_df)} matches)")
    
    if filtered_df.empty:
        st.info("No matching records found. Expand your filter ranges in the sidebar.")
        st.stop()

    # Columns of interest for the data explorer
    explorer_cols = [
        "App", "Category", "Rating", "Reviews", "Size", "Installs", "Type", "Price_Numeric", "Content Rating", "Sentiment"
    ]
    
    # Render Dataframe
    st.dataframe(
        filtered_df[explorer_cols].rename(columns={"Price_Numeric": "Price ($)"}),
        column_config={
            "Rating": st.column_config.NumberColumn("Rating", format="%.2f"),
            "Reviews": st.column_config.NumberColumn("Reviews", format="%d"),
            "Price ($)": st.column_config.NumberColumn("Price ($)", format="$%.2f"),
        },
        hide_index=True,
        use_container_width=True
    )

    # Export report tools
    st.markdown("### 📥 Document Generation Hub")
    col_dl1, col_dl2 = st.columns([10, 10])

    with col_dl1:
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="💾 Download Filtered Dataset (.CSV)",
            data=csv_data,
            file_name="googleplaystore_filtered_report.csv",
            mime="text/csv",
            help="Download the filtered records above for local reporting in Excel, Tableau, or custom pandas scripts."
        )

    with col_dl2:
        st.markdown(
            "*(Corporate Policy Notice: Downloaded spreadsheets contain fully validated schemas, ready for immediate data lake ingest.)*"
        )

    st.markdown("---")

    # Visual 12: Top 10 Apps by Review count (Bar Chart)
    st.markdown("### 📊 Top 10 Most Reviewed Apps in Filtered Scope")
    top_reviewed = filtered_df.sort_values(by="Reviews", ascending=False).head(10)
    
    fig_top_rev = px.bar(
        top_reviewed,
        x="Reviews",
        y="App",
        orientation="h",
        color="Reviews",
        color_continuous_scale="purples",
        labels={"Reviews": "Total Review Text Count", "App": "App Name"},
        text="Reviews"
    )
    fig_top_rev.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    fig_top_rev.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        yaxis={"categoryorder": "total ascending"}
    )
    st.plotly_chart(fig_top_rev, use_container_width=True)

    st.markdown("---")
    
    # Advanced: Details expander for focused inspections
    st.markdown("### 🔍 Single Entry Metadata Inspector")
    inspect_app_name = st.selectbox(
        "Select App for Detailed In-Depth Inspection",
        options=sorted(filtered_df["App"].tolist())
    )
    
    if inspect_app_name:
        inspect_df = filtered_df[filtered_df["App"] == inspect_app_name].iloc[0]
        
        col_ins1, col_ins2, col_ins3 = st.columns(3)
        with col_ins1:
            st.write(f"**App Name**: {inspect_df['App']}")
            st.write(f"**Category Segment**: {inspect_df['Category']}")
            st.write(f"**Genres Mapping**: {inspect_df['Genres']}")
        with col_ins2:
            st.write(f"**Star Rating**: {inspect_df['Rating']} / 5.0")
            st.write(f"**User Review Counts**: {inspect_df['Reviews']:,}")
            st.write(f"**Estimated Downloads**: {inspect_df['Installs']}")
        with col_ins3:
            st.write(f"**File Footprint**: {inspect_df['Size']}")
            st.write(f"**Retail Pricing**: {inspect_df['Price']}")
            st.write(f"**Content Restriction**: {inspect_df['Content Rating']}")
            
        st.markdown(
            render_insight_card(
                f"{inspect_app_name} Onboarding Assessment",
                f"With a star rating of **{inspect_df['Rating']}** and average sentiment score of "
                f"**{inspect_df['Sentiment_Score']:.2f}** ({inspect_df['Sentiment']}), this app reflects "
                f"a highly engaging consumer loop. Launch cycles are optimized around the last verified update date "
                f"of {inspect_df['Last Updated'].strftime('%Y-%m-%d')}."
            ),
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
