Spotify Listening History Analyzer

Project Overview

A web application that lets you upload your Spotify listening history (the ZIP file
provided by Spotify's "Download your data" service), analyzes your listening habits,
and visualizes the results in the browser. Originally a CustomTkinter desktop app,
the project was pivoted to a Streamlit-based web application for richer interactive
visualizations and easier sharing.

Primarily intended for personal use, skill demonstration, and analyzing friends'
listening histories.

How to Run

    pip install -r requirements.txt
    streamlit run app.py

The app opens automatically at http://localhost:8501.

Tech Stack
    • Streamlit — web UI
    • pandas   — data loading and analysis
    • Plotly   — interactive visualizations

Project Structure

    app.py                    Streamlit entry point
    src/data_loader.py        JSON loading + cleaning
    src/analyzer.py           Pure analysis functions (top lists, totals, weekday)
    .streamlit/config.toml    Spotify-themed dark mode
    data/                     Local sample data (not tracked in git)

Features
    • Upload Spotify listening history ZIP
    • Top N artists, tracks, and albums (configurable, 1–50)
    • Key metrics: total listening time, total plays, unique artists, date range
    • Listening hours by weekday (Plotly chart)
    • Horizontal bar charts for all top lists, Spotify-themed dark UI

Data Source

The application uses listening history data obtained directly from Spotify's official
data export service. The data is in JSON format and contains track name, artist,
album, timestamp, and milliseconds played, among other fields.

Version Control

Version control is managed using Git. The project repository is available at:
https://github.com/Cani41/Spotify_analytics.git

Development Status
    • Phase 0: Project setup, repository, initial UI                     — done
    • Phase 1: Data loading and basic analysis                           — done
    • Phase 2: Visualization (Plotly via Streamlit)                      — done
    • Phase 3: UI polish and documentation                               — in progress

Known Limitations
    • Supports only the standard Spotify listening history JSON files
      (Streaming_History_Audio_*.json).
    • Real-time data fetching via the Spotify API is not supported.
    • The full ZIP is loaded into memory; very large exports may be slow on
      low-memory machines.

Future Expansion Opportunities
    • Search functionality for specific tracks, artists, or patterns.
    • Monthly and yearly listening trend analysis.
    • Skip-rate / completion-rate analysis (uses ms_played + track duration).
    • Exporting analysis results as reports.
    • User customization options for themes and settings.
