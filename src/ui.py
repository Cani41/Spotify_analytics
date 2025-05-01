# src/ui.py
import customtkinter as ctk

class StartScreen(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.configure(fg_color="#191414")
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(10, lambda: self.attributes("-topmost", False))

        self.title("Spotify Analytics")
        self.geometry("600x400")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.frame = ctk.CTkFrame(master=self, fg_color="#191414")
        self.frame.pack(pady=50, padx=50, fill="both", expand=True)

        # Otsikkoteksti
        self.label = ctk.CTkLabel(master=self.frame,
                                  text="Spotify Analytics",
                                  font=("Helvetica", 24),
                                  text_color="#1DB954")
        self.label.pack(pady=20)

        # Start-painike
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

        # "Made by" -teksti alareunaan
        self.made_by_label = ctk.CTkLabel(master=self.frame,
                                          text="Made by\nSanteri Kananen",
                                          font=("Helvetica", 12),
                                          text_color="#dce8e1")
        self.made_by_label.pack(side="bottom", pady=(20, 20))  # pieni marginaali alas

    def on_start(self):
        print("Start button clicked")