

# src/analyzer.py

def get_top_artists(df, n=5):
    """Return the top n artists by play count."""
    return df['master_metadata_album_artist_name'].value_counts().head(n)

def get_top_tracks(df, n=5):
    """Return the top n tracks (track + artist) by play count."""
    if 'track_artist' not in df.columns:
        df['track_artist'] = df['master_metadata_track_name'] + " - " + df['master_metadata_album_artist_name']
    return df['track_artist'].value_counts().head(n)

def get_top_albums(df, n=5):
    """Return the top n albums (album + artist) by play count."""
    if 'album_artist' not in df.columns:
        df['album_artist'] = df['master_metadata_album_album_name'] + " - " + df['master_metadata_album_artist_name']
    return df['album_artist'].value_counts().head(n)