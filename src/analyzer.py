# -----------------------------------------------------------
# File name: analyzer.py
# Author: Santeri Kananen
# GitHub: https://github.com/Cani41
# Email: santerikananen@gmail.com
# Created: 01/05/2025
# Description: Functions for analyzing Spotify listening data
# -----------------------------------------------------------

import pandas as pd

WEEKDAY_ORDER = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]


def get_top_artists(df, n=5):
    """Return the top n artists by play count."""
    return df['master_metadata_album_artist_name'].value_counts().head(n)

def get_top_tracks(df, n=5):
    """Return the top n tracks (track + artist) by play count."""
    combined = (
        df['master_metadata_track_name']
        + " - "
        + df['master_metadata_album_artist_name']
    )
    return combined.value_counts().head(n)


def get_top_albums(df, n=5):
    """Return the top n albums (album + artist) by play count."""
    combined = (
        df['master_metadata_album_album_name']
        + " - "
        + df['master_metadata_album_artist_name']
    )
    return combined.value_counts().head(n)


def get_total_listening_ms(df):
    """Return total listening time in milliseconds."""
    if 'ms_played' not in df.columns:
        return 0
    return int(df['ms_played'].sum())


def get_weekday_listening_hours(df):
    """Return total listening hours grouped by weekday, ordered Mon..Sun."""
    if 'ts' not in df.columns or 'ms_played' not in df.columns:
        return pd.Series(dtype=float)
    weekday = df['ts'].dt.day_name()
    hours = df.groupby(weekday)['ms_played'].sum() / 3_600_000
    return hours.reindex(WEEKDAY_ORDER, fill_value=0)