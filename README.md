
# Listening Test Application

This application is a web-based listening test designed to evaluate emotional responses to music. Participants listen to a series of songs and assess each one based on four emotions: **Aggressive, Relaxed, Happy,** and **Sad**. Each emotion is rated on a scale from -3 (strongly opposed) to +3 (strongly present).


<img src="https://github.com/michelerossi1/listening_test_webAPP/blob/cc6afb9e418e8b73ebf12302c46fb743ad0ca8a0/images/screenshot_listening_test_zoom.png" alt="Description of image" width="50%"/>


## Features
- **Dynamic Audio Selection**: Randomized playlists are created from two parts of audio files.
- **User Evaluation Storage**: Each user's ratings are saved to a unique CSV file for later analysis.
- **Session Management**: User data is securely stored in sessions, ensuring smooth transitions between songs.
- **Progress and Guidance**: A progress bar and periodic messages help guide participants through the test.

## Getting Started
1. **Clone the repository** and install dependencies:
   ```bash
   git clone https://github.com/michelerossi1/listening_test_webAPP.git
   cd listening_test_webAPP
   pip install -r requirements.txt

2. **Run the app locally** on port 5000:
   ```bash
   python app.py

3. **Access the test** by navigating to http://localhost:5000.

