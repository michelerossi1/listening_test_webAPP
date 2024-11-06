# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 14:33:23 2024

@author: miche
"""


from flask import Flask, render_template, request, redirect, url_for, session
import os
import csv
import random
from datetime import datetime 


app = Flask(__name__)
app.secret_key = "secret_key"  # Required for session management
random_modification2 = 'random_modification2'

AUDIO_FOLDER = "static/music"
USER_EVALUATIONS_FOLDER = "user_evaluations"  # Folder to store individual user evaluation files

# Ensure the user evaluations folder exists
os.makedirs(USER_EVALUATIONS_FOLDER, exist_ok=True)

ORIGINAL_FOLDER = os.path.join(AUDIO_FOLDER, "original")
AUGMENTED_FOLDER = os.path.join(AUDIO_FOLDER, "augmented")

now = datetime.now()
# Format timestamp
TIMESTAMP = now.strftime("%d%b%Y_%I-%M").lower() + ('am' if now.hour < 12 else 'pm')

def get_audio_files():
    """Retrieve and shuffle .wav files from original and augmented folders separately."""
    
    # Get all .wav files in the original folder
    original_files = [os.path.join("original", f) for f in os.listdir(ORIGINAL_FOLDER) if f.endswith(".wav")]
    
    # Get all .wav files in each subfolder of the augmented folder
    augmented_files = []
    for subfolder in os.listdir(AUGMENTED_FOLDER):
        subfolder_path = os.path.join(AUGMENTED_FOLDER, subfolder)
        if os.path.isdir(subfolder_path):  # Only process directories
            augmented_files += [os.path.join("augmented", subfolder, f) 
                                for f in os.listdir(subfolder_path) if f.endswith(".wav")]
    
    # Shuffle the original and augmented lists separately
    random.shuffle(original_files)
    random.shuffle(augmented_files)
    
    # Combine the two lists with original files first
    return original_files + augmented_files


def save_evaluation(user_data, song, evaluation):
    """Save a song evaluation to a unique CSV file for each user in the user_evaluations folder."""
    # Create a unique filename for each user based on their name
    # Get current time
  # e.g., "04nov2024_10-19am" or "04nov2024_10-19pm"

    filename = f"{user_data['name']}_{user_data['age']}_{TIMESTAMP}.csv"
    csv_path = os.path.join(USER_EVALUATIONS_FOLDER, filename)

    # Check if the file already exists to determine if headers are needed
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Write header only if the file is new
        if not file_exists:
            writer.writerow(["Name", "Age", "Gender", "Song", "Aggressive", "Relaxed", "Happy", "Sad"])
        
        # Write evaluation data to the file
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
    # Always refresh the audio files list on each visit to this route
    session['audio_files'] = get_audio_files()
    session['current_song_index'] = 0

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

    # Calculate total songs
    total_songs = len(audio_files)
    
    # Check for messages at 1/4, 1/2, and 3/4
    message = ""
    if current_song_index == total_songs // 4 -1:
        message = "You've reached 1/4 of the songs. Take a 5-minute break to rest your ears!"
    elif current_song_index == total_songs // 2 -1:
        message = "You've reached half of the songs. Take a 5-minute break to rest your ears!"
    elif current_song_index == (3 * total_songs) // 4 -1:
        message = "You've reached 3/4 of the songs. Take a 5-minute break to rest your ears!"

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
        save_evaluation(session.get("user", {}), audio_files[current_song_index], evaluation)


        # Move to the next song
        session['current_song_index'] += 1
        
        
        # If there's a message to display, render the message page
        if message:
            return render_template("message.html", message=message)
        
        
        
        if session['current_song_index'] < len(audio_files):           
                       
            return redirect(url_for('play_song'))
        else:
            # Reset for a new session or user
            session['current_song_index'] = 0
            return "Thank you for evaluating all songs!"
        
        
    # Get current song if no message needs to be shown
    current_song = audio_files[current_song_index]
    current_song_path = f"{AUDIO_FOLDER}/{current_song}"
    user = session.get("user", {})

    return render_template("index.html", show_player=True, song_path=current_song_path, user=user)


if __name__ == "__main__":
    
    #app.run(debug=True)   
    
    app.run(host="0.0.0.0", port=5000, debug=True)
    
    

