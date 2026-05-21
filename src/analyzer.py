# -----------------------------------------------------------
# File name: analyzer.py
# Author: Santeri Kananen
# GitHub: https://github.com/Cani41
# Email: santerikananen@gmail.com
# Created: 01/05/2025
# Description: Functions for analyzing Spotify listening data
# -----------------------------------------------------------

from dataclasses import dataclass

import pandas as pd

WEEKDAY_ORDER = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]


def _top_by_keys(df, name_col, artist_col=None, n=5):
    """Top n entries grouped by name_col (and optionally artist_col).

    Returns a DataFrame with columns: name, artist, plays, hours.
    For artist top lists (no artist_col), the artist column is None.
    """
    music = df.dropna(subset=[name_col])
    group_cols = [name_col] if artist_col is None else [name_col, artist_col]
    grouped = music.groupby(group_cols)['ms_played'].agg(plays='count', ms='sum')
    grouped['hours'] = grouped['ms'] / 3_600_000
    result = grouped.sort_values('plays', ascending=False).head(n).reset_index()
    rename_map = {name_col: 'name'}
    if artist_col:
        rename_map[artist_col] = 'artist'
    result = result.rename(columns=rename_map)
    if artist_col is None:
        result['artist'] = None
    return result[['name', 'artist', 'plays', 'hours']]


def get_top_artists(df, n=5):
    """Top n artists with plays + listening hours."""
    return _top_by_keys(df, 'master_metadata_album_artist_name', n=n)


def get_top_tracks(df, n=5):
    """Top n tracks with track name, artist, plays + hours."""
    return _top_by_keys(
        df,
        'master_metadata_track_name',
        'master_metadata_album_artist_name',
        n=n,
    )


def get_top_albums(df, n=5):
    """Top n albums with album name, artist, plays + hours."""
    return _top_by_keys(
        df,
        'master_metadata_album_album_name',
        'master_metadata_album_artist_name',
        n=n,
    )


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


def get_monthly_listening_hours(df):
    """Return total listening hours grouped by month, with a DatetimeIndex
    (one timestamp per month-start) so the result plots directly as a time series."""
    if 'ts' not in df.columns or 'ms_played' not in df.columns or df.empty:
        return pd.Series(dtype=float)
    period = df['ts'].dt.to_period('M')
    hours = df.groupby(period)['ms_played'].sum() / 3_600_000
    hours.index = hours.index.to_timestamp()
    return hours


# --- Aika ja käyttötiheys ---

def get_active_days(df):
    """Number of distinct calendar days with any listening."""
    if 'ts' not in df.columns or 'ms_played' not in df.columns:
        return 0
    listened = df[df['ms_played'] > 0]
    return int(listened['ts'].dt.date.nunique())


def get_daily_average_hours(df):
    """Average listening hours across days where there was any listening."""
    active = get_active_days(df)
    if active == 0:
        return 0.0
    return (get_total_listening_ms(df) / 3_600_000) / active


def get_longest_streak(df):
    """Longest run of consecutive calendar days with any listening."""
    if 'ts' not in df.columns or 'ms_played' not in df.columns:
        return 0
    listened = df[df['ms_played'] > 0]
    if listened.empty:
        return 0
    dates = sorted(set(listened['ts'].dt.date))
    longest = current = 1
    for prev, curr in zip(dates, dates[1:]):
        current = current + 1 if (curr - prev).days == 1 else 1
        longest = max(longest, current)
    return longest


def get_most_active_day(df):
    """Return (date, hours) for the single calendar day with most listening."""
    if 'ts' not in df.columns or 'ms_played' not in df.columns or df.empty:
        return None
    by_day = df.groupby(df['ts'].dt.date)['ms_played'].sum()
    if by_day.empty:
        return None
    day = by_day.idxmax()
    return day, by_day.loc[day] / 3_600_000


def get_most_active_year(df):
    """Return (year, hours) for the year with most listening."""
    if 'ts' not in df.columns or 'ms_played' not in df.columns or df.empty:
        return None
    by_year = df.groupby(df['ts'].dt.year)['ms_played'].sum()
    if by_year.empty:
        return None
    year = by_year.idxmax()
    return int(year), by_year.loc[year] / 3_600_000


# --- Musiikkivalikoima ---

def get_unique_artists(df):
    """Distinct artist count, excluding NaN."""
    col = 'master_metadata_album_artist_name'
    if col not in df.columns:
        return 0
    return int(df[col].dropna().nunique())


def get_unique_tracks(df):
    """Distinct (track, artist) pairs, excluding rows with missing track name."""
    if 'master_metadata_track_name' not in df.columns:
        return 0
    music = df.dropna(subset=['master_metadata_track_name'])
    return int(
        music[['master_metadata_track_name', 'master_metadata_album_artist_name']]
        .drop_duplicates()
        .shape[0]
    )


def get_unique_albums(df):
    """Distinct (album, artist) pairs, excluding rows with missing album name."""
    if 'master_metadata_album_album_name' not in df.columns:
        return 0
    music = df.dropna(subset=['master_metadata_album_album_name'])
    return int(
        music[['master_metadata_album_album_name', 'master_metadata_album_artist_name']]
        .drop_duplicates()
        .shape[0]
    )


def get_one_time_song_pct(df):
    """Percent of unique (track, artist) pairs that were played exactly once."""
    if 'master_metadata_track_name' not in df.columns:
        return 0.0
    counts = df.groupby(
        ['master_metadata_track_name', 'master_metadata_album_artist_name']
    ).size()
    if counts.empty:
        return 0.0
    return float((counts == 1).sum() / len(counts) * 100)


def get_top_artist_share(df):
    """Return (artist, share_pct) for the artist with most listening time."""
    if (
        'master_metadata_album_artist_name' not in df.columns
        or 'ms_played' not in df.columns
    ):
        return None
    by_artist = df.groupby('master_metadata_album_artist_name')['ms_played'].sum()
    total = by_artist.sum()
    if by_artist.empty or total == 0:
        return None
    artist = by_artist.idxmax()
    return artist, float(by_artist.loc[artist] / total * 100)


def get_tracks_per_artist(df):
    """Average number of distinct tracks per distinct artist."""
    if (
        'master_metadata_track_name' not in df.columns
        or 'master_metadata_album_artist_name' not in df.columns
    ):
        return 0.0
    music = df.dropna(subset=['master_metadata_album_artist_name'])
    artists = music['master_metadata_album_artist_name'].nunique()
    if artists == 0:
        return 0.0
    return get_unique_tracks(df) / artists


# --- Käyttäytyminen ---

SKIP_THRESHOLD_MS = 30_000


def get_skip_rate(df):
    """Percent of plays where less than SKIP_THRESHOLD_MS were listened to."""
    if 'ms_played' not in df.columns or df.empty:
        return 0.0
    return float((df['ms_played'] < SKIP_THRESHOLD_MS).sum() / len(df) * 100)


def get_completion_rate(df):
    """Percent of plays where reason_end == 'trackdone'.

    Returns None if reason_end is missing (e.g. stale cache or older export)
    so the UI can distinguish 'missing data' from a real 0%.
    """
    if 'reason_end' not in df.columns:
        return None
    if df.empty:
        return 0.0
    return float((df['reason_end'] == 'trackdone').sum() / len(df) * 100)


def get_peak_hour(df):
    """Return (hour, share_pct) for the clock hour with most listening time."""
    if 'ts' not in df.columns or 'ms_played' not in df.columns or df.empty:
        return None
    by_hour = df.groupby(df['ts'].dt.hour)['ms_played'].sum()
    total = by_hour.sum()
    if by_hour.empty or total == 0:
        return None
    hour = by_hour.idxmax()
    return int(hour), float(by_hour.loc[hour] / total * 100)


# --- Aggregated metrics container ---

@dataclass
class AnalyticsMetrics:
    """All metrics computed from one (filtered) listening-history DataFrame.

    A single immutable result object the analytics view can read from,
    and a natural target for unit tests: build a small DataFrame, call
    compute_all_metrics, assert on returned fields.
    """
    # Date context
    date_min: pd.Timestamp
    date_max: pd.Timestamp

    # Hero / overview totals
    total_ms: int
    total_hours: float
    total_days: float
    total_plays: int
    unique_artists: int
    unique_tracks: int

    # Top lists — each a DataFrame: name, artist, plays, hours
    top_artists: pd.DataFrame
    top_tracks: pd.DataFrame
    top_albums: pd.DataFrame

    # Time & frequency
    active_days: int
    daily_avg_hours: float
    longest_streak: int
    most_active_day: tuple | None   # (date, hours) or None
    most_active_year: tuple | None  # (year, hours) or None

    # Music catalog
    unique_albums: int
    one_time_song_pct: float
    top_artist_share: tuple | None  # (artist, share_pct) or None
    tracks_per_artist: float

    # Behavior
    skip_rate: float
    completion_rate: float | None  # None if reason_end column missing
    peak_hour: tuple | None        # (hour, share_pct) or None

    # Time series — monthly listening hours over the (filtered) period
    monthly_hours: pd.Series


def compute_all_metrics(df, n: int = 10) -> AnalyticsMetrics:
    """Run every analytics function over `df` and bundle results into one object.

    Args:
        df: cleaned streaming history (already date-filtered)
        n:  size of the top-artist/track/album lists
    """
    total_ms = get_total_listening_ms(df)
    total_hours = total_ms / 3_600_000

    return AnalyticsMetrics(
        date_min=df["ts"].min(),
        date_max=df["ts"].max(),
        total_ms=total_ms,
        total_hours=total_hours,
        total_days=total_hours / 24,
        total_plays=len(df),
        unique_artists=get_unique_artists(df),
        unique_tracks=get_unique_tracks(df),
        top_artists=get_top_artists(df, n=n),
        top_tracks=get_top_tracks(df, n=n),
        top_albums=get_top_albums(df, n=n),
        active_days=get_active_days(df),
        daily_avg_hours=get_daily_average_hours(df),
        longest_streak=get_longest_streak(df),
        most_active_day=get_most_active_day(df),
        most_active_year=get_most_active_year(df),
        unique_albums=get_unique_albums(df),
        one_time_song_pct=get_one_time_song_pct(df),
        top_artist_share=get_top_artist_share(df),
        tracks_per_artist=get_tracks_per_artist(df),
        skip_rate=get_skip_rate(df),
        completion_rate=get_completion_rate(df),
        peak_hour=get_peak_hour(df),
        monthly_hours=get_monthly_listening_hours(df),
    )