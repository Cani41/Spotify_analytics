# -----------------------------------------------------------
# File name: app.py
# Author: Santeri Kananen
# GitHub: https://github.com/Cani41
# Email: santerikananen@gmail.com
# Description: Streamlit-based Spotify listening history analyzer
# -----------------------------------------------------------

import html as _html
import io
import json
import os
import tempfile
import zipfile
from datetime import date, timedelta
from pathlib import Path

import plotly.express as px
import streamlit as st

from src.analyzer import compute_all_metrics
from src.data_loader import clean_data, load_streaming_data

SPOTIFY_GREEN = "#1DB954"
GITHUB_USER = "Cani41"
GITHUB_REPO = "https://github.com/Cani41/Spotify_analytics"
STATIC_DIR = Path(__file__).parent / "static"

st.set_page_config(
    page_title="Spotify Analytics",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data(show_spinner=False)
def _read_static(filename: str) -> str:
    """Read a text file from static/ (cached, since contents are static)."""
    return (STATIC_DIR / filename).read_text(encoding="utf-8")


def inject_css(filename: str) -> None:
    """Inject the CSS from static/<filename> into the current page."""
    st.markdown(f"<style>{_read_static(filename)}</style>", unsafe_allow_html=True)


inject_css("styles.css")


@st.cache_data(show_spinner=False)
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
    is_horizontal = orientation == "h"
    if is_horizontal:
        fig = px.bar(x=x, y=y, orientation="h", labels={"x": value_label, "y": ""})
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=max(220, 28 * len(y) + 60))
    else:
        fig = px.bar(x=x, y=y, labels={"x": "", "y": value_label})

    font_family = "Manrope, -apple-system, BlinkMacSystemFont, sans-serif"
    fig.update_traces(
        marker_color=SPOTIFY_GREEN,
        marker_line_width=0,
        hovertemplate=(
            "<b>%{y}</b><br>%{x}<extra></extra>"
            if is_horizontal
            else "<b>%{x}</b><br>%{y}<extra></extra>"
        ),
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=font_family, color="#b5b5b5", size=11),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showgrid=is_horizontal,
            gridcolor="rgba(255,255,255,0.05)",
            tickfont=dict(family=font_family, color="#b5b5b5", size=11),
            title_font=dict(family=font_family, color="#6f6f6f", size=10),
        ),
        yaxis=dict(
            zeroline=False,
            showline=False,
            showgrid=not is_horizontal,
            gridcolor="rgba(255,255,255,0.05)",
            tickfont=dict(family=font_family, color="#b5b5b5", size=11),
            title_font=dict(family=font_family, color="#6f6f6f", size=10),
        ),
        hoverlabel=dict(
            bgcolor="#131313",
            bordercolor=SPOTIFY_GREEN,
            font=dict(family=font_family, size=12, color="#ededed"),
        ),
    )
    return fig


def styled_line(x, y, value_label):
    """Spotify-themed line chart with subtle area fill — for time-series trends."""
    font_family = "Manrope, -apple-system, BlinkMacSystemFont, sans-serif"
    fig = px.line(x=x, y=y, labels={"x": "", "y": value_label})
    fig.update_traces(
        line=dict(color=SPOTIFY_GREEN, width=2),
        fill="tozeroy",
        fillcolor="rgba(29, 185, 84, 0.14)",
        mode="lines+markers",
        marker=dict(size=4, color=SPOTIFY_GREEN),
        hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.1f} h<extra></extra>",
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=font_family, color="#b5b5b5", size=11),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showgrid=False,
            tickfont=dict(family=font_family, color="#b5b5b5", size=11),
            title_font=dict(family=font_family, color="#6f6f6f", size=10),
        ),
        yaxis=dict(
            zeroline=False,
            showline=False,
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            tickfont=dict(family=font_family, color="#b5b5b5", size=11),
            title_font=dict(family=font_family, color="#6f6f6f", size=10),
        ),
        hoverlabel=dict(
            bgcolor="#131313",
            bordercolor=SPOTIFY_GREEN,
            font=dict(family=font_family, size=12, color="#ededed"),
        ),
    )
    return fig


def fmt_date(dt):
    return f"{dt.day}.{dt.month}.{dt.year}"


def fmt_hours(hours):
    if hours >= 10:
        return f"{hours:,.0f} h"
    if hours >= 1:
        return f"{hours:.1f} h"
    return f"{hours * 60:.0f} min"


def render_top_list(df_top, title, pad_artist: bool = True):
    """Render a top-N list. If pad_artist is True, missing artist rows get a
    blank placeholder so all three columns stay vertically aligned. Set False
    in compact mode where height parity matters less than density."""
    st.subheader(title)
    items = []
    for rank, (_, row) in enumerate(df_top.iterrows(), start=1):
        name = _html.escape(str(row['name']))
        artist = row['artist']
        if artist:
            artist_html = f"<div class='top-item-artist'>{_html.escape(str(artist))}</div>"
        elif pad_artist:
            artist_html = "<div class='top-item-artist'>&nbsp;</div>"
        else:
            artist_html = ""
        plays = int(row['plays'])
        hours = float(row['hours'])
        items.append(
            f"<div class='top-item'>"
            f"<div class='top-item-rank'>{rank}</div>"
            f"<div class='top-item-body'>"
            f"<div class='top-item-name'>{name}</div>"
            f"{artist_html}"
            f"<div class='top-item-stats'>{plays:,} plays · {hours:,.1f} h</div>"
            f"</div>"
            f"</div>"
        )
    st.markdown(f"<div class='top-list'>{''.join(items)}</div>", unsafe_allow_html=True)


def handle_upload(uploaded_file):
    """Try to parse uploaded ZIP, store cleaned DataFrame in session_state."""
    loading = st.empty()
    loading.markdown(
        '<div class="loading-state">'
        '<div class="loading-spinner"></div>'
        '<span>Loading data…</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    try:
        df = load_and_clean(uploaded_file.getvalue())
    except zipfile.BadZipFile:
        loading.empty()
        st.error("That file does not appear to be a valid ZIP archive.")
        return
    except json.JSONDecodeError as e:
        loading.empty()
        st.error(f"One of the JSON files is malformed: {e}")
        return

    if df is None:
        loading.empty()
        st.error("No 'Streaming_History_Audio_*.json' files found in the ZIP.")
        return

    loading.empty()
    st.session_state["df_clean"] = df
    st.rerun()


# ============================================================
# LANDING PAGE
# ============================================================

if "df_clean" not in st.session_state:
    st.markdown(
        """
        <div class="landing-hero">
          <h1 class="landing-display" style="color: var(--accent) !important;">Spotify Analytics</h1>
          <div class="landing-rule"><span class="dot"></span></div>
          <div class="landing-dek">Decode your listening history — top tracks, artists, habits and the year-over-year shape of your taste.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(
            """
            <div class="anim-step-1">
              <div class="landing-upload-intro">Upload the <strong>ZIP</strong> from Spotify's <em>Download your data</em> service to get started.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="anim-step-2">', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Spotify data ZIP",
            type=["zip"],
            label_visibility="collapsed",
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if uploaded is not None:
            handle_upload(uploaded)

        st.markdown(
            f"""
            <div class="anim-step-3">
              <div class="landing-footer">
                <span>Built by</span>
                <a href="https://github.com/{GITHUB_USER}">{GITHUB_USER}</a>
                <span class="sep"></span>
                <a href="{GITHUB_REPO}">Source</a>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.stop()


# ============================================================
# ANALYTICS VIEW
# ============================================================

df_full = st.session_state["df_clean"]

# Reserve the main area with a loading state so sidebar + main view appear
# in sync (without sidebar popping in seconds before the analytics).
analytics_loading = st.empty()
analytics_loading.markdown(
    '<div class="loading-state">'
    '<div class="loading-spinner"></div>'
    '<span>Preparing your analytics…</span>'
    '</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Settings")
    min_date = df_full["ts"].min().date()
    max_date = df_full["ts"].max().date()

    if "date_range" not in st.session_state:
        st.session_state["date_range"] = (min_date, max_date)

    quick_ranges = {
        "7 days":    (max_date - timedelta(days=7),   max_date),
        "30 days":   (max_date - timedelta(days=30),  max_date),
        "3 months":  (max_date - timedelta(days=90),  max_date),
        "12 months": (max_date - timedelta(days=365), max_date),
        "This year": (date(max_date.year, 1, 1),      max_date),
        "All time":  (min_date,                       max_date),
    }

    def _apply_preset() -> None:
        """Sync date_range from the selected quick-range pill, clamped to data bounds."""
        preset = st.session_state.get("quick_range_preset")
        if preset:
            start, end = quick_ranges[preset]
            st.session_state["date_range"] = (max(start, min_date), min(end, max_date))

    st.pills(
        "Quick range",
        options=list(quick_ranges.keys()),
        selection_mode="single",
        default=None,
        key="quick_range_preset",
        on_change=_apply_preset,
    )

    date_range = st.date_input(
        "Date range",
        format="DD.MM.YYYY",
        key="date_range",
    )
    n = st.slider("List size", min_value=1, max_value=50, value=10)

    st.markdown("---")
    if st.button("Change data", use_container_width=True, type="primary"):
        del st.session_state["df_clean"]
        st.rerun()

inject_css("compact.css")

df_clean = df_full
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    df_clean = df_clean[
        (df_clean["ts"].dt.date >= start_date)
        & (df_clean["ts"].dt.date <= end_date)
    ]

if df_clean.empty:
    analytics_loading.warning("No listening data in the selected range.")
    st.stop()

metrics = compute_all_metrics(df_clean, n=n)
analytics_loading.empty()

st.markdown(
    f'<div class="analytics-eyebrow">{fmt_date(metrics.date_min)} — {fmt_date(metrics.date_max)}</div>',
    unsafe_allow_html=True,
)
st.title("Spotify Analytics")

total_value = (
    f"{metrics.total_days:,.1f} d" if metrics.total_hours >= 48
    else f"{metrics.total_hours:,.1f} h"
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total listening", total_value)
c2.metric("Total plays", f"{metrics.total_plays:,}")
c3.metric("Unique artists", f"{metrics.unique_artists:,}")
c4.metric("Unique songs", f"{metrics.unique_tracks:,}")


col_a, col_t, col_al, col_d = st.columns([1.1, 1.1, 1.1, 1])
with col_a:
    render_top_list(metrics.top_artists, "Top Artists")
with col_t:
    render_top_list(metrics.top_tracks, "Top Tracks")
with col_al:
    render_top_list(metrics.top_albums, "Top Albums")
with col_d:
    tab_time, tab_catalog, tab_behavior = st.tabs(["Time", "Catalog", "Behavior"])

    with tab_time:
        st.metric("Active days", f"{metrics.active_days:,}")
        st.metric("Daily average", fmt_hours(metrics.daily_avg_hours))
        st.metric("Longest streak", f"{metrics.longest_streak:,} d")
        if metrics.most_active_day is not None:
            day, hours = metrics.most_active_day
            st.metric("Most active day", fmt_date(day), delta=fmt_hours(hours), delta_color="off")
        if metrics.most_active_year is not None:
            year, hours = metrics.most_active_year
            st.metric("Most active year", str(year), delta=fmt_hours(hours), delta_color="off")

        if not metrics.monthly_hours.empty:
            st.markdown("##### Monthly listening")
            fig_monthly = styled_line(
                metrics.monthly_hours.index,
                metrics.monthly_hours.values,
                "Hours",
            )
            fig_monthly.update_layout(height=170)
            st.plotly_chart(fig_monthly, use_container_width=True)

    with tab_catalog:
        st.metric("Unique albums", f"{metrics.unique_albums:,}")
        st.metric("One-time songs", f"{metrics.one_time_song_pct:.1f} %")
        if metrics.top_artist_share is not None:
            artist, share = metrics.top_artist_share
            st.metric(
                "Top artist",
                artist,
                delta=f"{share:.1f} % of time",
                delta_color="off",
            )
        st.metric("Tracks per artist", f"{metrics.tracks_per_artist:.1f}")

    with tab_behavior:
        st.metric("Skip rate", f"{metrics.skip_rate:.1f} %")
        if metrics.completion_rate is None:
            st.metric(
                "Completion rate",
                "—",
                delta="reason_end missing",
                delta_color="off",
            )
        else:
            st.metric("Completion rate", f"{metrics.completion_rate:.1f} %")
        if metrics.peak_hour is not None:
            hour, share = metrics.peak_hour
            st.metric(
                "Peak hour",
                f"{hour}:00",
                delta=f"{share:.1f} % of plays",
                delta_color="off",
            )
