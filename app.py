# -----------------------------------------------------------
# File name: app.py
# Author: Santeri Kananen
# GitHub: https://github.com/Cani41
# Email: santerikananen@gmail.com
# Description: Streamlit-based Spotify listening history analyzer
# -----------------------------------------------------------

import io
import json
import os
import tempfile
import zipfile

import plotly.express as px
import streamlit as st

from src.analyzer import (
    get_top_albums,
    get_top_artists,
    get_top_tracks,
    get_total_listening_ms,
    get_weekday_listening_hours,
)
from src.data_loader import clean_data, load_streaming_data

SPOTIFY_GREEN = "#1DB954"

st.set_page_config(page_title="Spotify Analytics", layout="wide")


@st.cache_data(show_spinner="Loading streaming data…")
def load_and_clean(file_bytes: bytes):
    """Extract ZIP from memory, load all audio JSONs, clean. Cached by bytes."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(io.BytesIO(file_bytes), "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        audio_files = []
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.startswith("Streaming_History_Audio_") and file.endswith(".json"):
                    audio_files.append(os.path.join(root, file))

        if not audio_files:
            return None

        df = load_streaming_data(audio_files)
        return clean_data(df)


def styled_bar(x, y, value_label, orientation="v"):
    if orientation == "h":
        fig = px.bar(x=x, y=y, orientation="h", labels={"x": value_label, "y": ""})
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=max(220, 28 * len(y) + 60))
    else:
        fig = px.bar(x=x, y=y, labels={"x": "", "y": value_label})
    fig.update_traces(marker_color=SPOTIFY_GREEN)
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


st.title("Spotify Analytics")
st.caption("Upload your Spotify data export ZIP to analyze your listening history.")

with st.sidebar:
    st.header("Data")
    uploaded_file = st.file_uploader(
        "Spotify data ZIP",
        type=["zip"],
        help="The file you receive from Spotify's 'Download your data' service.",
    )

    if uploaded_file is not None:
        try:
            df_clean = load_and_clean(uploaded_file.getvalue())
        except zipfile.BadZipFile:
            st.error("That file does not appear to be a valid ZIP archive.")
            st.stop()
        except json.JSONDecodeError as e:
            st.error(f"One of the JSON files is malformed: {e}")
            st.stop()

        if df_clean is None:
            st.error("No 'Streaming_History_Audio_*.json' files found in the ZIP.")
            st.stop()

        st.session_state["df_clean"] = df_clean
        st.success(f"Loaded {len(df_clean):,} rows.")

    st.header("Settings")
    n = st.slider("Top N", min_value=1, max_value=50, value=10)

if "df_clean" not in st.session_state:
    st.info("Upload your Spotify ZIP in the sidebar to begin.")
    st.stop()

df_clean = st.session_state["df_clean"]

total_ms = get_total_listening_ms(df_clean)
total_hours = total_ms / 3_600_000
total_days = total_hours / 24
date_min = df_clean["ts"].min()
date_max = df_clean["ts"].max()

c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Total listening",
    f"{total_days:,.1f} d" if total_hours >= 48 else f"{total_hours:,.1f} h",
)
c2.metric("Total plays", f"{len(df_clean):,}")
c3.metric(
    "Unique artists",
    f"{df_clean['master_metadata_album_artist_name'].nunique():,}",
)
c4.metric("Date range", f"{date_min.date()} → {date_max.date()}")

st.subheader("Listening by weekday")
weekday_hours = get_weekday_listening_hours(df_clean)
st.plotly_chart(
    styled_bar(weekday_hours.index, weekday_hours.values, "Hours"),
    use_container_width=True,
)

top_artists = get_top_artists(df_clean, n=n)
top_tracks = get_top_tracks(df_clean, n=n)
top_albums = get_top_albums(df_clean, n=n)

col_a, col_t, col_al = st.columns(3)

with col_a:
    st.subheader("Top Artists")
    st.plotly_chart(
        styled_bar(top_artists.values, top_artists.index, "Plays", orientation="h"),
        use_container_width=True,
    )

with col_t:
    st.subheader("Top Tracks")
    st.plotly_chart(
        styled_bar(top_tracks.values, top_tracks.index, "Plays", orientation="h"),
        use_container_width=True,
    )

with col_al:
    st.subheader("Top Albums")
    st.plotly_chart(
        styled_bar(top_albums.values, top_albums.index, "Plays", orientation="h"),
        use_container_width=True,
    )
