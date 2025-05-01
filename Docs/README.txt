Spotify Listening History Analyzer

Project Overview

This project aims to develop a clean and minimalist application that allows users to upload their Spotify listening history files (.json format), analyze their listening habits, and visualize the results in a clear graphical user interface (GUI). The initial focus is on building a simple and usable application, with flexibility for more advanced features in later phases.

The application is primarily intended for personal use, skill demonstration during job interviews, and analyzing friends’ listening histories. A long-term goal is to implement an efficient search functionality for easier data exploration.

Project Scope

In the initial development phases (0–2), the application will support:
	•	Uploading Spotify listening history files.
	•	Performing basic statistical analyses (top tracks, top artists, total listening time, listening activity by weekday).
	•	Displaying clear and simple visualizations.

More advanced features such as detailed trends and search functionality are planned for future development.

Data Source

The application uses listening history data obtained directly from Spotify’s official data export service. The data is in JSON format and contains details like track name, artist, and timestamp. The exact structure will be verified with real data samples.

Version Control

Version control is managed using Git. The project repository is available at:
https://github.com/Cani41/Spotify_analytics.git

Features
	•	Upload Spotify listening history (.json)
	•	Basic statistical analyses:
	•	Top artists
	•	Top tracks
	•	Total listening time
	•	Listening activity by day of the week
	•	Clear and simple visualizations

Development Timeline
	•	Phase 0: Project setup, GitHub repository, basic GUI creation
	•	Phase 1: Data loading and basic analysis
	•	Phase 2: Data visualization and integration with the GUI
	•	Phase 3: UI polish and final documentation

Long-term goals include implementing search functionality, more advanced analytics, and exporting capabilities.

Known Limitations
	•	Currently supports only standard Spotify listening history JSON files.
	•	Real-time data fetching via Spotify API is not yet supported.

Potential Challenges
	•	Variations in Spotify data format.
	•	Handling large listening history files efficiently.
	•	Maintaining a clean and simple user interface as features expand.
	•	Developing a fast and intuitive search function in the future.
	•	Minor GUI differences across operating systems.

Future Expansion Opportunities
	•	Search functionality for specific tracks, artists, or patterns.
	•	Monthly and yearly listening trend analysis.
	•	Interactive visualizations with libraries like Plotly.
	•	Handling and merging multiple history files.
	•	Exporting analysis results as reports.
	•	User customization options for themes and settings.