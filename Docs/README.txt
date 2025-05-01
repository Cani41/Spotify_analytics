**Spotify Listening History Analyzer**

**Project Goal and Scope**

The primary objective of this project is to develop a clean and minimalist application that allows users to upload their Spotify listening history files (.json format), analyze their listening habits, and visualize the results in an intuitive graphical user interface (GUI). The project will initially focus on a simple and clear start screen and basic analysis features, while maintaining flexibility for more complex functionalities as the project evolves.

The application is primarily intended for personal use and skill demonstration purposes, for example during job interviews. It may also be used to analyze the listening history of friends. A long-term goal is to implement an efficient and user-friendly search functionality, enabling users to easily explore and retrieve specific information from their listening history.



**Project Scope**

In the initial phases (phases 0–2), the focus of the project is to develop a fully functional application that allows users to upload Spotify listening history files, perform simple analyses, and visualize the results in a straightforward and clear manner. The goal is to create a clean and usable core application without getting overwhelmed by deeper analytical features at this stage.

More advanced analyses, additional insights, and the implementation of a powerful search functionality are intentionally postponed to future development phases. This ensures that the early versions remain focused, maintainable, and demonstrable, while leaving room for meaningful future improvements.

**Intended Use and Users**

The application is primarily intended for personal use to analyze and visualize Spotify listening history. It is also designed to demonstrate programming skills during job interviews. In addition, the application may be used to analyze the listening histories of friends or other users by loading different data files.

**Data Source and Format**

The application will use Spotify listening history files obtained directly from Spotify’s official data export service. The files are provided in JSON format and typically contain structured information about each listening event, such as the track name, artist, and timestamp.
The exact structure of the data will be verified once a sample file is available to ensure compatibility with the data processing pipeline.


**Features**
	•	Upload Spotify listening history files (.json)
	•	Basic statistical analyses:
	•	Top artists
	•	Top tracks
	•	Total listening time
	•	Listening activity by day of the week
	•	Clear visualizations of the data

**Future Improvements**
	•	Genre analysis if genre metadata is available
	•	Monthly and yearly listening trend reports
	•	More interactive visualizations
	•	Support for merging multiple history files

**Known Limitations**
	•	Currently supports only Spotify’s standard listening history JSON file format
	•	No support yet for real-time API data fetching