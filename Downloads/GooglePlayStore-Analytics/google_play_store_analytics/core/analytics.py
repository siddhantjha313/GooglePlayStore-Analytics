"""
Core Analytics and Business Logic Module.

Responsible for calculating advanced metrics, market shares, correlation matrices,
sentiment distributions, and developer benchmarks from the preprocessed Google Play Store data.
"""

import logging
from typing import Dict, Any, List
import pandas as pd
import numpy as np

logger = logging.getLogger("AnalyticsEngine")


def get_kpi_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate the global high-level KPI metrics for the executive dashboard."""
    try:
        total_apps = int(df["App"].nunique())
        avg_rating = float(df["Rating"].mean()) if len(df) > 0 else 0.0
        total_installs = int(df["Installs_Numeric"].sum())
        total_reviews = int(df["Reviews"].sum())
        
        # Free vs Paid percentage
        type_counts = df["Type"].value_counts()
        free_count = int(type_counts.get("Free", 0))
        paid_count = int(type_counts.get("Paid", 0))
        total_types = free_count + paid_count
        free_ratio = (free_count / total_types * 100) if total_types > 0 else 0.0
        
        # Average paid app price
        paid_df = df[df["Type"] == "Paid"]
        avg_price = float(paid_df["Price_Numeric"].mean()) if len(paid_df) > 0 else 0.0
        
        # Sentiment metrics
        positive_sentiment_ratio = 0.0
        if "Sentiment" in df.columns and len(df) > 0:
            pos_count = int((df["Sentiment"] == "Positive").sum())
            positive_sentiment_ratio = (pos_count / len(df)) * 100

        return {
            "total_apps": total_apps,
            "avg_rating": round(avg_rating, 2),
            "total_installs": total_installs,
            "total_reviews": total_reviews,
            "free_ratio_percent": round(free_ratio, 1),
            "avg_paid_price": round(avg_price, 2),
            "positive_sentiment_percent": round(positive_sentiment_ratio, 1)
        }
    except Exception as e:
        logger.error(f"Error calculating KPI metrics: {e}")
        return {}


def calculate_category_summaries(df: pd.DataFrame) -> pd.DataFrame:
    """Group data by Category and compute high-value aggregate metrics."""
    try:
        if df.empty:
            return pd.DataFrame()
            
        summary = df.groupby("Category").agg(
            App_Count=("App", "count"),
            Total_Installs=("Installs_Numeric", "sum"),
            Avg_Rating=("Rating", "mean"),
            Avg_Reviews=("Reviews", "mean"),
            Avg_Size_MB=("Size_MB", "mean"),
            Avg_Price=("Price_Numeric", "mean")
        ).reset_index()
        
        # Calculate market share based on install volume
        global_installs = summary["Total_Installs"].sum()
        summary["Install_Market_Share_Percent"] = (
            (summary["Total_Installs"] / global_installs * 100) if global_installs > 0 else 0.0
        )
        summary["Install_Market_Share_Percent"] = summary["Install_Market_Share_Percent"].round(2)
        summary["Avg_Rating"] = summary["Avg_Rating"].round(2)
        summary["Avg_Reviews"] = summary["Avg_Reviews"].round(0)
        summary["Avg_Size_MB"] = summary["Avg_Size_MB"].round(1)
        summary["Avg_Price"] = summary["Avg_Price"].round(2)
        
        return summary.sort_values(by="Total_Installs", ascending=False)
    except Exception as e:
        logger.error(f"Error calculating category summaries: {e}")
        return pd.DataFrame()


def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Compute the Pearson correlation matrix between major numerical features."""
    try:
        cols = ["Rating", "Reviews", "Installs_Numeric", "Size_MB", "Price_Numeric", "Sentiment_Score"]
        # Filter columns that exist
        valid_cols = [c for c in cols if c in df.columns]
        if len(valid_cols) < 2:
            return pd.DataFrame()
            
        corr = df[valid_cols].corr(method="pearson")
        # Rename index/columns for executive-level presentation
        display_names = {
            "Rating": "App Rating",
            "Reviews": "Review Count",
            "Installs_Numeric": "Download Count",
            "Size_MB": "File Size (MB)",
            "Price_Numeric": "Retail Price ($)",
            "Sentiment_Score": "User Sentiment Score"
        }
        corr.rename(index=display_names, columns=display_names, inplace=True)
        return corr.round(3)
    except Exception as e:
        logger.error(f"Error computing correlation matrix: {e}")
        return pd.DataFrame()


def generate_benchmark_insights(df: pd.DataFrame, category: str) -> Dict[str, Any]:
    """
    Generate tailored business recommendations and benchmarks for a given app category.
    
    Helps developers decide on optimal price, file size, and launch metrics.
    """
    try:
        cat_df = df[df["Category"] == category] if category != "All Categories" else df
        if cat_df.empty:
            return {"status": "No data available"}

        # Highly rated apps benchmark (Rating >= 4.4)
        top_apps = cat_df[cat_df["Rating"] >= 4.4]
        if top_apps.empty:
            top_apps = cat_df.sort_values(by="Rating", ascending=False).head(5)

        ideal_size_min = float(top_apps["Size_MB"].quantile(0.25))
        ideal_size_max = float(top_apps["Size_MB"].quantile(0.75))
        ideal_price = float(top_apps["Price_Numeric"].mean())
        ideal_content_rating = str(top_apps["Content Rating"].mode().iloc[0]) if len(top_apps["Content Rating"]) > 0 else "Everyone"
        
        # Paid apps potential
        paid_cat_df = cat_df[cat_df["Type"] == "Paid"]
        paid_viability = "Moderate"
        if len(paid_cat_df) > 0:
            avg_paid_rating = paid_cat_df["Rating"].mean()
            if avg_paid_rating > 4.4:
                paid_viability = "High (Users are highly receptive to premium quality)"
            elif avg_paid_rating < 4.0:
                paid_viability = "Low (Premium entries receive critical feedback)"
        else:
            paid_viability = "High Potential (Uncharted premium market space)"

        # Sentiment benchmark
        avg_sentiment = float(cat_df["Sentiment_Score"].mean())
        sentiment_label = "Highly Favorable" if avg_sentiment > 0.4 else "Favorable" if avg_sentiment > 0.1 else "Neutral/Mixed" if avg_sentiment > -0.1 else "Critical"

        return {
            "ideal_size_range_mb": (round(ideal_size_min, 1), round(ideal_size_max, 1)),
            "suggested_price": round(ideal_price, 2),
            "recommended_target_audience": ideal_content_rating,
            "monetization_viability": paid_viability,
            "general_sentiment_index": round(avg_sentiment, 2),
            "sentiment_label": sentiment_label,
            "recommendation": (
                f"For launching a successful entry in '{category}', aim for a file footprint of "
                f"{round(ideal_size_min, 1)}-{round(ideal_size_max, 1)} MB. Keep the entry optimized for "
                f"'{ideal_content_rating}'. Premium pricing benchmarks indicate an entry point of ${round(ideal_price, 2)} "
                f"if launching paid. Focus on user onboarding to align with the category's '{sentiment_label}' review profile."
            )
        }
    except Exception as e:
        logger.error(f"Error generating category benchmarks: {e}")
        return {}
