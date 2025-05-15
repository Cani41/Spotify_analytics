# src/ui.py
# User interface module for Spotify Listening History Analyzer
import customtkinter as ctk
import tkinter.filedialog as filedialog
import zipfile
import os
import tempfile
from src.data_loader import load_streaming_data, clean_data
from src.analyzer import get_top_artists, get_top_tracks, get_top_albums

# Main start screen window
class StartScreen(ctk.CTk):

    def __init__(self):
        super().__init__()
        # Configure start window appearance and properties
        self.configure(fg_color="#191414")
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(10, lambda: self.attributes("-topmost", False))

        self.title("Spotify Analytics")
        self.geometry("600x400")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Create the main frame container
        self.frame = ctk.CTkFrame(master=self, fg_color="#191414")
        self.frame.pack(pady=50, padx=50)

        # Add header label
        self.label = ctk.CTkLabel(master=self.frame,
                                  text="Spotify Analytics",
                                  font=("Helvetica", 24),
                                  text_color="#dce8e1")
        self.label.pack(pady=20)

        # Add Start button
        self.start_button = ctk.CTkButton(master=self.frame,
                                  text="Start",
                                  command=self.on_start,
                                  fg_color="#1DB954",
                                  hover_color="#1a5e34",
                                  font=("Helvetica", 16),
                                  height=40,
                                  width=100,
                                  corner_radius=20)
        self.start_button.pack(pady=(110, 10))

        # Add Settings button
        self.settings_button = ctk.CTkButton(master=self.frame,
                                  text="Settings",
                                  command=self.on_settings,
                                  fg_color="#535353",
                                  hover_color="#3c3c3c",
                                  font=("Helvetica", 16),
                                  height=40,
                                  width=100,
                                  corner_radius=20)
        self.settings_button.pack(pady=(10, 10))

        # Add 'Made by' footer label
        self.made_by_label = ctk.CTkLabel(master=self.frame,
                                          text="Made by\nSanteri Kananen",
                                          font=("Helvetica", 12),
                                          text_color="#dce8e1")
        self.made_by_label.pack(side="bottom", pady=(5, 10))
    def on_start(self):
        self.withdraw()
        self.new_window = FileSelectionWindow(parent=self)

    def on_settings(self):
        self.withdraw()
        self.new_window = SettingsWindow(parent=self)


# Window for selecting Spotify data ZIP file
class FileSelectionWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Configure file selection window appearance and properties
        self.title("File Selection")
        self.geometry("500x300")
        self.configure(fg_color="#191414")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Add header label
        self.label = ctk.CTkLabel(master=self,
                                  text="Select Spotify ZIP File",
                                  font=("Helvetica", 18),
                                  text_color="#dce8e1")
        self.label.pack(pady=(20, 5))

        # Add 'Choose File' button
        self.choose_file_button = ctk.CTkButton(master=self,
                                                text="Choose File",
                                                command=self.choose_file,
                                                fg_color="#1DB954",
                                                hover_color="#1a5e34",
                                                font=("Helvetica", 16),
                                                height=40,
                                                width=100,
                                                corner_radius=20)
        self.choose_file_button.pack(pady=(120, 10))

    # Handle file selection and extraction of audio streaming data
    def choose_file(self):
        file_path = filedialog.askopenfilename(
            title="Select your Spotify Data ZIP file",
            filetypes=[("ZIP files", "*.zip")]
        )
        if file_path:
            print(f"Selected file: {file_path}")

            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()
            print(f"Temporary extraction folder: {temp_dir}")

            # Extract the zip file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Filter and print only relevant audio streaming history JSON files
            selected_files = []
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.startswith("Streaming_History_Audio_") and file.endswith(".json"):
                        full_path = os.path.join(root, file)
                        selected_files.append(full_path)

            if selected_files:
                print("Accepted files:")
                for f in selected_files:
                    print(f"- {f}")
                # Load data into a DataFrame
                df = load_streaming_data(selected_files)
                df_clean = clean_data(df)
                print(f"Loaded {len(df)} rows of streaming data.")
                print(f"Cleaned data ready with {len(df_clean)} rows.")
                self.destroy()
                self.success_window = LoadSuccessWindow()
                self.success_window.df_clean = df_clean
            else:
                print("No suitable files found.")
        else:
            print("No file selected.")

    # Handle window closing and return to start screen
    def on_close(self):
        self.destroy()
        self.parent.deiconify()

class LoadSuccessWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Data Loaded")
        self.geometry("400x200")
        self.configure(fg_color="#191414")

        # Success message
        self.label = ctk.CTkLabel(master=self,
                                  text="Data loaded successfully!",
                                  font=("Helvetica", 20),
                                  text_color="#dce8e1")
        self.label.pack(pady=(40, 20))

        # Analyze button
        self.analyze_button = ctk.CTkButton(master=self,
                                            text="Analyze",
                                            command=self.on_analyze,
                                            fg_color="#1DB954",
                                            hover_color="#1a5e34",
                                            font=("Helvetica", 16),
                                            height=40,
                                            width=120,
                                            corner_radius=20)
        self.analyze_button.pack(pady=10)

    def on_analyze(self):
        self.destroy()
        self.analysis_window = AnalysisWindow(self.df_clean)


# Analyze window
class AnalysisWindow(ctk.CTkToplevel):
    def __init__(self, df_clean):
        super().__init__()

        self.title("Analysis Results")
        self.geometry("800x400")
        self.configure(fg_color="#191414")

        # Analyze data using analyzer module
        top_artists = get_top_artists(df_clean, n=5)
        top_tracks = get_top_tracks(df_clean, n=5)
        top_albums = get_top_albums(df_clean, n=5)

        # Create a frame to hold top lists side by side
        self.list_frame = ctk.CTkFrame(master=self, fg_color="#191414")
        self.list_frame.pack(pady=20, padx=20, expand=True, fill="both")

        # Display top artists
        artist_text = "Top Artists:\n" + "\n".join([f"{i+1}. {artist}" for i, artist in enumerate(top_artists.index)])
        self.artist_label = ctk.CTkLabel(master=self.list_frame, text=artist_text, font=("Helvetica", 16), text_color="#dce8e1", justify="left")
        self.artist_label.pack(side="left", expand=True, padx=10)

        # Display top tracks with play counts
        track_text = "Top Tracks:\n" + "\n".join([
            f"{i+1}. {track} ({top_tracks.iloc[i]})"
            for i, track in enumerate(top_tracks.index)
        ])
        self.track_label = ctk.CTkLabel(master=self.list_frame, text=track_text, font=("Helvetica", 16), text_color="#dce8e1", justify="left")
        self.track_label.pack(side="left", expand=True, padx=10)

        # Display top albums with play counts
        album_text = "Top Albums:\n" + "\n".join([
            f"{i+1}. {album} ({top_albums.iloc[i]})"
            for i, album in enumerate(top_albums.index)
        ])
        self.album_label = ctk.CTkLabel(master=self.list_frame, text=album_text, font=("Helvetica", 16), text_color="#dce8e1", justify="left")
        self.album_label.pack(side="left", expand=True, padx=10)

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.title("Settings")
        self.geometry("400x300")
        self.configure(fg_color="#191414")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Header label
        self.label = ctk.CTkLabel(master=self,
                                  text="Settings (Coming Soon)",
                                  font=("Helvetica", 20),
                                  text_color="#dce8e1")
        self.label.pack(pady=(50, 20))

        # Back button
        self.back_button = ctk.CTkButton(master=self,
                                         text="Back",
                                         command=self.on_close,
                                         fg_color="#535353",
                                         hover_color="#3c3c3c",
                                         font=("Helvetica", 16),
                                         height=40,
                                         width=100,
                                         corner_radius=20)
        self.back_button.pack(pady=20)

    def on_close(self):
        self.destroy()
        self.parent.deiconify()