
# Listening Test Application

This application is a web-based listening test designed to evaluate emotional responses to music. Participants listen to a series of songs and assess each one based on four emotions: **Aggressive, Relaxed, Happy,** and **Sad**. Each emotion is rated on a scale from -3 (strongly opposed) to +3 (strongly present).

Currently, the list of song paths to be evaluated is divided into two separate lists **hardcoded in the app.py file**. When the user selects an option (part 1 or part 2) at the beginning of the interaction, only one of these lists is considered and shuffled before presenting the songs to be evaluated.

If you want to use different songs for the test, please load your songs into the static/music/augmented folder. Then, **define a function to scan all the folders and subfolders you've added**, which returns a list of paths for all the songs.

---

<img src="https://github.com/michelerossi1/listening_test_webAPP/blob/cc6afb9e418e8b73ebf12302c46fb743ad0ca8a0/images/screenshot_listening_test_zoom.png" alt="Description of image" width="45%"/>

---

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




