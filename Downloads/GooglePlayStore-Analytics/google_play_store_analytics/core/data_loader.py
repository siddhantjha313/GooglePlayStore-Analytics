"""
Core Data Loader Module.

Responsible for loading, cleaning, preprocessing, and validating the
Google Play Store dataset. Implements Streamlit caching, logging, type hints,
and rigorous error handling.
"""

import logging
import os
import re
from typing import Optional
import pandas as pd
import numpy as np
import streamlit as st

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("DataLoader")


def clean_installs(val: str) -> float:
    """Convert install string (e.g., '1,000,000+') to a numeric float value."""
    try:
        if pd.isna(val) or val == "":
            return 0.0
        # Remove commas, plus signs, and any trailing spaces
        cleaned = re.sub(r"[,\+ ]", "", str(val))
        return float(cleaned)
    except Exception as e:
        logger.warning(f"Error cleaning installs value '{val}': {e}")
        return 0.0


def clean_price(val: str) -> float:
    """Convert price string (e.g., '$4.99') to a float value."""
    try:
        if pd.isna(val) or str(val).strip() == "0" or str(val).strip().lower() == "free":
            return 0.0
        # Remove currency symbols and whitespace
        cleaned = re.sub(r"[\$ ]", "", str(val))
        return float(cleaned)
    except Exception as e:
        logger.warning(f"Error cleaning price value '{val}': {e}")
        return 0.0


def clean_size(val: str) -> Optional[float]:
    """Convert size string (e.g., '76M', '120k') to size in Megabytes (float)."""
    try:
        if pd.isna(val):
            return None
        val_str = str(val).strip().upper()
        if "VARIES WITH DEVICE" in val_str or val_str == "":
            return None
        
        if "M" in val_str:
            # Megabytes
            cleaned = re.sub(r"[M ]", "", val_str)
            return float(cleaned)
        elif "K" in val_str:
            # Kilobytes -> convert to MB
            cleaned = re.sub(r"[K ]", "", val_str)
            return float(cleaned) / 1024.0
        else:
            # Pure numeric assumed MB
            return float(re.sub(r"[^0-9\.]", "", val_str))
    except Exception as e:
        logger.warning(f"Error cleaning size value '{val}': {e}")
        return None


@st.cache_data(show_spinner=True)
def load_and_preprocess_data(file_path: str) -> pd.DataFrame:
    """
    Load and clean the Google Play Store dataset.

    Uses Streamlit caching to speed up page reloads. Performs data cleaning,
    type casting, and missing value imputation.
    """
    logger.info(f"Loading data from {file_path}")

    # 1. Verification of file presence
    if not os.path.exists(file_path):
        error_msg = f"Data file not found at path: {file_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        df = pd.read_csv(
            file_path,
            encoding="utf-8",
            engine="python",
            on_bad_lines="warn"
        )
    except Exception as e:
        logger.error(f"Failed to read CSV file: {e}")
        raise e

    # 2. Schema Validation
    required_cols = [
        "App", "Category", "Rating", "Reviews", "Size",
        "Installs", "Type", "Price", "Content Rating"
    ]
    for col in required_cols:
        if col not in df.columns:
            # Try matching with whitespace or case-insensitivity
            matching_cols = [c for c in df.columns if c.strip().lower() == col.strip().lower()]
            if matching_cols:
                df.rename(columns={matching_cols[0]: col}, inplace=True)
            else:
                logger.error(f"Missing required column: {col}")
                # Create default mock column if missing
                df[col] = np.nan

    logger.info("Starting data preprocessing operations")

    # 3. Data Cleaning
    # Convert Rating to numeric, handle bounds
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Rating"] = df["Rating"].apply(lambda x: np.clip(x, 1.0, 5.0) if not pd.isna(x) else np.nan)
    
    # Convert Reviews to numeric
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0).astype(int)
    
    # Clean Installs and Price
    df["Installs_Numeric"] = df["Installs"].apply(clean_installs)
    df["Price_Numeric"] = df["Price"].apply(clean_price)
    
    # Clean Size and calculate SizeBytes (in Megabytes)
    df["Size_MB"] = df["Size"].apply(clean_size)
    
    # Impute missing Size_MB with the category median (robust preprocessing)
    category_medians = df.groupby("Category")["Size_MB"].transform("median")
    overall_median = df["Size_MB"].median() if not df["Size_MB"].isna().all() else 25.0
    df["Size_MB"] = df["Size_MB"].fillna(category_medians).fillna(overall_median)
    
    # Impute missing Rating with the category median rating
    category_rating_medians = df.groupby("Category")["Rating"].transform("median")
    overall_rating_median = df["Rating"].median() if not df["Rating"].isna().all() else 4.3
    df["Rating"] = df["Rating"].fillna(category_rating_medians).fillna(overall_rating_median)
    
    # Format Type securely
    df["Type"] = df["Type"].fillna("Free")
    df.loc[df["Price_Numeric"] > 0, "Type"] = "Paid"
    df.loc[df["Price_Numeric"] == 0, "Type"] = "Free"
    
    # Standardize Content Rating
    df["Content Rating"] = df["Content Rating"].fillna("Everyone")
    
    # Convert Last Updated to Datetime
    df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")
    # Impute missing dates with a fallback date
    df["Last Updated"] = df["Last Updated"].fillna(pd.Timestamp("2026-01-01"))
    
    # Add sentiment column if missing or preprocess existing sentiment
    if "Reviews Sentiment" in df.columns:
        df["Sentiment"] = df["Reviews Sentiment"].fillna("Neutral")
    else:
        df["Sentiment"] = "Neutral"
        
    if "Sentiment Score" in df.columns:
        df["Sentiment_Score"] = pd.to_numeric(df["Sentiment Score"], errors="coerce").fillna(0.0)
    else:
        # Synthesize a realistic Sentiment Score based on Rating
        # Rating 4.5 -> ~0.5, Rating 3.0 -> ~0.0, Rating 1.5 -> ~-0.5
        df["Sentiment_Score"] = df["Rating"].apply(lambda r: (r - 3.5) / 2.0 + np.random.uniform(-0.1, 0.1))
        df["Sentiment_Score"] = df["Sentiment_Score"].clip(-1.0, 1.0)
        df.loc[df["Sentiment_Score"] > 0.15, "Sentiment"] = "Positive"
        df.loc[df["Sentiment_Score"] < -0.15, "Sentiment"] = "Negative"
        df.loc[(df["Sentiment_Score"] >= -0.15) & (df["Sentiment_Score"] <= 0.15), "Sentiment"] = "Neutral"

    logger.info(f"Preprocessing completed. Loaded {len(df)} records successfully.")
    return df
