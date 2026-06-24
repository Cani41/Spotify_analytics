# Spotify Listening Analytics

A Streamlit web app that turns your Spotify listening-history export into an
interactive analytics dashboard. Upload the ZIP from Spotify's "Download your
data", pick a date range, and explore your habits: top tracks, artists and
albums, total listening time, streaks, trends and more.

> Personal project. Runs locally; not deployed.

<!-- Add a screenshot here, e.g. ![Dashboard](docs/screenshot.png) -->

## Features

- **Upload & parse** the official Spotify "Download your data" export
  (`Streaming_History_Audio_*.json` inside the ZIP)
- **Date-range and Top-N filters** in the sidebar (quick-range presets + custom dates)
- **Top lists** — tracks, artists and albums with play counts and progress bars
- **Listening totals** — minutes/hours, play counts, active days, daily average
- **Time patterns** — peak hour, listening by weekday, monthly trend (time series),
  longest daily streak, most active day and year
- **Catalog insight** — unique artists/tracks/albums, one-time-song %, top-artist
  share, tracks per artist
- **Behavior** — skip rate and completion rate (`reason_end == "trackdone"`)
- **Spotify-themed dark UI** (custom CSS, Plotly charts)

## Tech stack

- **Streamlit** — web UI
- **pandas** — data loading, cleaning, aggregation
- **Plotly Express** — interactive charts

No database and no backend service — three dependencies (`requirements.txt`).

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501.

To get your data: in Spotify, go to **Account → Privacy → Download your data** and
request your account data (the extended streaming history can take a few days to
arrive). Unzip it and upload the ZIP in the app.

## Project structure

```
app.py                  Streamlit UI: upload + analytics views
src/data_loader.py      JSON loading, cleaning, timezone normalization (UTC -> Europe/Helsinki)
src/analyzer.py         Pure metric functions + AnalyticsMetrics dataclass (compute_all_metrics)
static/                 Spotify-themed CSS
.streamlit/config.toml  Dark theme (Spotify green #1DB954)
```

The analysis layer (`src/analyzer.py`) is pure functions: a cleaned DataFrame goes
in, an immutable `AnalyticsMetrics` comes out, which keeps it easy to test and reuse
independently of the UI.

## Notes & limitations

- Supports the standard `Streaming_History_Audio_*.json` files.
- No live Spotify API — works entirely from the offline data export.
- The full export is loaded into memory; very large histories may be slow on
  low-memory machines.

## License

See [LICENSE](LICENSE).
