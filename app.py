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

AUDIO_FOLDER = "static/music"
USER_EVALUATIONS_FOLDER = "user_evaluations"  # Folder to store individual user evaluation files

# Ensure the user evaluations folder exists
os.makedirs(USER_EVALUATIONS_FOLDER, exist_ok=True)

# thi folder contains also the orignal songs
AUGMENTED_FOLDER = os.path.join(AUDIO_FOLDER, "augmented")

# get time to save the time in the csv file
now = datetime.now()
TIMESTAMP = now.strftime("%d%b%Y_%I-%M").lower() + ('am' if now.hour < 12 else 'pm')


# got this audio files 
audio_path_part1 = ['augmented\\8__sad\\sad2_low_pass.wav', 'augmented\\3__happy\\happy_time_stretch_low.wav', 'augmented\\0__original\\0__relaxed2_original_then.wav', 'augmented\\5__aggressive\\aggressive2_pitch_shift_low.wav', 'augmented\\1__aggressive\\aggressive_time_stretch_high.wav', 'augmented\\2__relaxed\\relaxed_saturation.wav', 'augmented\\1__aggressive\\aggressive_resampling.wav', 'augmented\\3__happy\\happy_resampling.wav', 'augmented\\7__happy\\happy2_compressor.wav', 'augmented\\3__happy\\happy_reverb.wav', 'augmented\\2__relaxed\\relaxed_pitch_shift_high.wav', 'augmented\\0__original\\0__aggressive2_original_then.wav', 'augmented\\5__aggressive\\aggressive2_high_pass.wav', 'augmented\\2__relaxed\\relaxed_noise_addition.wav', 'augmented\\2__relaxed\\relaxed_reverb.wav', 'augmented\\2__relaxed\\relaxed_high_pass.wav', 'augmented\\2__relaxed\\relaxed_time_stretch_low.wav', 'augmented\\1__aggressive\\aggressive_pitch_shift_low.wav', 'augmented\\5__aggressive\\aggressive2_low_pass.wav', 'augmented\\0__original\\0__sad2_original_then.wav', 'augmented\\7__happy\\happy2_pitch_shift_low.wav', 'augmented\\4__sad\\sad_saturation.wav', 'augmented\\6__relaxed\\relaxed2_noise_addition.wav', 'augmented\\5__aggressive\\aggressive2_time_stretch_low.wav', 'augmented\\8__sad\\sad2_reverb.wav', 'augmented\\5__aggressive\\aggressive2_reverb.wav', 'augmented\\4__sad\\sad_noise_addition.wav', 'augmented\\1__aggressive\\aggressive_time_stretch_low.wav', 'augmented\\4__sad\\sad_pitch_shift_low.wav', 'augmented\\4__sad\\sad_pitch_shift_high.wav', 'augmented\\3__happy\\happy_noise_addition.wav', 'augmented\\7__happy\\happy2_pitch_shift_high.wav', 'augmented\\3__happy\\happy_pitch_shift_high.wav', 'augmented\\7__happy\\happy2_high_pass.wav', 'augmented\\2__relaxed\\relaxed_pitch_shift_low.wav', 'augmented\\5__aggressive\\aggressive2_resampling.wav', 'augmented\\1__aggressive\\aggressive_pitch_shift_high.wav', 'augmented\\8__sad\\sad2_saturation.wav', 'augmented\\5__aggressive\\aggressive2_saturation.wav', 'augmented\\7__happy\\happy2_saturation.wav', 'augmented\\6__relaxed\\relaxed2_time_stretch_low.wav', 'augmented\\6__relaxed\\relaxed2_compressor.wav', 'augmented\\3__happy\\happy_low_pass.wav', 'augmented\\7__happy\\happy2_time_stretch_high.wav', 'augmented\\6__relaxed\\relaxed2_saturation.wav', 'augmented\\1__aggressive\\aggressive_saturation.wav', 'augmented\\7__happy\\happy2_time_stretch_low.wav', 'augmented\\6__relaxed\\relaxed2_time_stretch_high.wav']
audio_path_part2 = ['augmented\\5__aggressive\\aggressive2_time_stretch_high.wav', 'augmented\\6__relaxed\\relaxed2_pitch_shift_low.wav', 'augmented\\2__relaxed\\relaxed_resampling.wav', 'augmented\\4__sad\\sad_reverb.wav', 'augmented\\4__sad\\sad_high_pass.wav', 'augmented\\4__sad\\sad_time_stretch_high.wav', 'augmented\\8__sad\\sad2_time_stretch_high.wav', 'augmented\\2__relaxed\\relaxed_compressor.wav', 'augmented\\7__happy\\happy2_noise_addition.wav', 'augmented\\8__sad\\sad2_time_stretch_low.wav', 'augmented\\0__original\\0__aggressive_origina_then.wav', 'augmented\\5__aggressive\\aggressive2_pitch_shift_high.wav', 'augmented\\2__relaxed\\relaxed_time_stretch_high.wav', 'augmented\\3__happy\\happy_saturation.wav', 'augmented\\5__aggressive\\aggressive2_compressor.wav', 'augmented\\3__happy\\happy_compressor.wav', 'augmented\\1__aggressive\\aggressive_low_pass.wav', 'augmented\\6__relaxed\\relaxed2_low_pass.wav', 'augmented\\3__happy\\happy_high_pass.wav', 'augmented\\4__sad\\sad_resampling.wav', 'augmented\\5__aggressive\\aggressive2_noise_addition.wav', 'augmented\\7__happy\\happy2_resampling.wav', 'augmented\\7__happy\\happy2_reverb.wav', 'augmented\\0__original\\0__happy2_original_then.wav', 'augmented\\6__relaxed\\relaxed2_resampling.wav', 'augmented\\4__sad\\sad_low_pass.wav', 'augmented\\2__relaxed\\relaxed_low_pass.wav', 'augmented\\1__aggressive\\aggressive_noise_addition.wav', 'augmented\\8__sad\\sad2_resampling.wav', 'augmented\\1__aggressive\\aggressive_compressor.wav', 'augmented\\6__relaxed\\relaxed2_high_pass.wav', 'augmented\\6__relaxed\\relaxed2_reverb.wav', 'augmented\\4__sad\\sad_compressor.wav', 'augmented\\8__sad\\sad2_compressor.wav', 'augmented\\0__original\\0__relaxed_original_then.wav', 'augmented\\0__original\\0__happy_original_then.wav', 'augmented\\1__aggressive\\aggressive_reverb.wav', 'augmented\\4__sad\\sad_time_stretch_low.wav', 'augmented\\8__sad\\sad2_pitch_shift_high.wav', 'augmented\\1__aggressive\\aggressive_high_pass.wav', 'augmented\\8__sad\\sad2_high_pass.wav', 'augmented\\7__happy\\happy2_low_pass.wav', 'augmented\\3__happy\\happy_pitch_shift_low.wav', 'augmented\\0__original\\0__sad_original_then.wav', 'augmented\\6__relaxed\\relaxed2_pitch_shift_high.wav', 'augmented\\3__happy\\happy_time_stretch_high.wav', 'augmented\\8__sad\\sad2_noise_addition.wav', 'augmented\\8__sad\\sad2_pitch_shift_low.wav']

# fake audio paths to make tests
#audio_path_part1 = ['augmented\\8__sad\\sad2_low_pass.wav','augmented\\8__sad\\sad2_low_pass.wav','augmented\\8__sad\\sad2_low_pass.wav','augmented\\8__sad\\sad2_low_pass.wav','augmented\\8__sad\\sad2_low_pass.wav','augmented\\8__sad\\sad2_low_pass.wav','augmented\\8__sad\\sad2_low_pass.wav','augmented\\8__sad\\sad2_low_pass.wav','augmented\\8__sad\\sad2_low_pass.wav','augmented\\8__sad\\sad2_low_pass.wav']
#audio_path_part2 = ['augmented\\5__aggressive\\aggressive2_time_stretch_high.wav','augmented\\5__aggressive\\aggressive2_time_stretch_high.wav','augmented\\5__aggressive\\aggressive2_time_stretch_high.wav','augmented\\5__aggressive\\aggressive2_time_stretch_high.wav','augmented\\5__aggressive\\aggressive2_time_stretch_high.wav','augmented\\5__aggressive\\aggressive2_time_stretch_high.wav','augmented\\5__aggressive\\aggressive2_time_stretch_high.wav','augmented\\5__aggressive\\aggressive2_time_stretch_high.wav','augmented\\5__aggressive\\aggressive2_time_stretch_high.wav','augmented\\5__aggressive\\aggressive2_time_stretch_high.wav']

# define a play_song function if you want to retreve the audio paths from the folders
#def get_songs():
#    # go throug all the folderas and subfolders..
#    return song_path_list

def save_evaluation(user_data, song, evaluation):
    """Save a song evaluation to a unique CSV file for each user in the user_evaluations folder."""
    # Create a unique filename for each user based on their name
    # Get current time
  # e.g., "04nov2024_10-19am" or "04nov2024_10-19pm"

    filename = f"{user_data['name']}_{user_data['age']}_{TIMESTAMP}_{session['part_selection']}.csv"
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
    if request.method == "POST":
        # Get form data        
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        part_selection = request.form.get("part_selection")
        
        # Store user details in session to retain them across requests
        session['user'] = {"name": name, "age": age, "gender": gender}
        
        if part_selection == "part1":
            session['audio_files'] = audio_path_part1
        elif part_selection == "part2":
            session['audio_files'] = audio_path_part2
        else:
            session['audio_files'] = []
            
        # shuffle audio files
        random.shuffle(session['audio_files'])
            
        # new put here the loadin gof the audio files
        session['current_song_index'] = 0
        
        # save for the csv file name
        session['part_selection'] = part_selection
        
        
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
    if current_song_index == total_songs // 2 -1:
        message = "You've reached half of the songs. Take a 5-minute break to rest your ears!"

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
    
    

