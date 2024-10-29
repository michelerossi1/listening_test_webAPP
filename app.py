# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 14:33:23 2024

@author: miche
"""

from flask import Flask, render_template, request, redirect, url_for, session
import os
import csv

app = Flask(__name__)
app.secret_key = "secret_key"  # Required for session management

AUDIO_FOLDER = "static/music"
EVALUATION_FILE = "evaluations.csv"  # The CSV file where evaluations will be stored


def get_audio_files():
    """Retrieve all .wav files from the AUDIO_FOLDER directory."""
    return [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(".wav")]


def save_evaluation(user_data, song, evaluation):
    """Save a song evaluation to a CSV file."""
    file_exists = os.path.isfile(EVALUATION_FILE)
    with open(EVALUATION_FILE, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        
        # If the file does not exist, write the header row
        if not file_exists:
            writer.writerow(["Name", "Age", "Gender", "Song", "Aggressive", "Relaxed", "Happy", "Sad"])
        
        # Write the evaluation data
        writer.writerow([
            user_data["name"],
            user_data["age"],
            user_data["gender"],
            song,
            evaluation["aggressive"],
            evaluation["relaxed"],
            evaluation["happy"],
            evaluation["sad"]
        ])


@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize session variables for the current song index and user info
    if 'current_song_index' not in session:
        session['current_song_index'] = 0
        session['audio_files'] = get_audio_files()

    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        
        # Store user details in session to retain them across requests
        session['user'] = {"name": name, "age": age, "gender": gender}
        
        return redirect(url_for('play_song'))

    return render_template("index.html", show_player=False)


@app.route("/play", methods=["GET", "POST"])
def play_song():
    # Check if there are any audio files
    if not session['audio_files']:
        return "No songs available."

    current_song_index = session.get('current_song_index', 0)
    audio_files = session['audio_files']

    # Get current song
    current_song = audio_files[current_song_index]
    current_song_path = f"{AUDIO_FOLDER}/{current_song}"

    # Get user data from session
    user = session.get("user", {})

    if request.method == "POST":
        # Get slider values from evaluation form
        aggressive = request.form.get("aggressive")
        relaxed = request.form.get("relaxed")
        happy = request.form.get("happy")
        sad = request.form.get("sad")
        
        # Prepare the evaluation data
        evaluation = {
            "aggressive": aggressive,
            "relaxed": relaxed,
            "happy": happy,
            "sad": sad
        }

        # Save the evaluation data to a file
        save_evaluation(user, current_song, evaluation)

        # Move to the next song
        session['current_song_index'] += 1
        if session['current_song_index'] < len(audio_files):
            return redirect(url_for('play_song'))
        else:
            # Reset for a new session or user
            session['current_song_index'] = 0
            return "Thank you for evaluating all songs!"

    return render_template("index.html", show_player=True, song_path=current_song_path, user=user)


if __name__ == "__main__":
    app.run(debug=True)


