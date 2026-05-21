# -----------------------------------------------------------
# File name: data_loader.py
# Author: Santeri Kananen
# GitHub: https://github.com/Cani41
# Email: santerikananen@gmail.com
# Created: 01/05/2025
# Description: Functions for loading and cleaning Spotify streaming data
# -----------------------------------------------------------
import json
import re

import pandas as pd


def clean_track_name(name):
    """
    Clean track name by removing parentheses content and anything after ' - '.
    """
    if pd.isnull(name):
        return name
    # Remove text inside parentheses
    name = re.sub(r'\s*\([^)]*\)', '', name)
    # Remove text after a dash, like " - Remastered"
    name = re.split(r'\s*-\s*', name)[0]
    return name.strip()

def load_streaming_data(file_paths):
    """
    Load and combine streaming history data from multiple JSON files into a single DataFrame.

    Args:
        file_paths (list): List of file paths to the JSON files.

    Returns:
        pd.DataFrame: Combined DataFrame containing all streaming events.
    """
    all_data = []

    for path in file_paths:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)

    df = pd.DataFrame(all_data)
    return df

def clean_data(df):
    """
    Select essential columns for analysis:
    track name, artist, album, timestamp, and duration.

    Args:
        df (pd.DataFrame): Full streaming history DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame with selected columns only.
    """
    essential_columns = [
        "master_metadata_track_name",
        "master_metadata_album_artist_name",
        "master_metadata_album_album_name",
        "ts",
        "ms_played",
        "reason_end",
    ]
    # Keep only columns that exist in the dataset
    columns_to_keep = [col for col in essential_columns if col in df.columns]
    df_clean = df[columns_to_keep].copy()

    # Clean track names for analysis
    if "master_metadata_track_name" in df_clean.columns:
        df_clean['master_metadata_track_name'] = df_clean['master_metadata_track_name'].apply(clean_track_name)

    # Convert timestamp once to local time so downstream analytics
    # (weekday, hour, day, year) match the user's wall-clock perception.
    if "ts" in df_clean.columns:
        df_clean['ts'] = (
            pd.to_datetime(df_clean['ts'], utc=True)
            .dt.tz_convert('Europe/Helsinki')
        )

    return df_clean