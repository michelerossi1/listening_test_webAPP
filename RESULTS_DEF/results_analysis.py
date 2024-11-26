# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 08:28:06 2024

@author: miche
"""

# %%

import pandas as pd
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


AUGMENTATIONS = ['original', 'pitch_shift_low', 'pitch_shift_high', 'time_stretch_low', 'time_stretch_high', 'noise_addition', 'reverb','saturation', 'low_pass','high_pass', 'compressor', 'resampling']
EMOTIONS = ['Aggressive', 'Relaxed', 'Happy', 'Sad']

# folder with all the csv files
root_path = r"C:\Users\miche\Desktop\webAPP_listening\app_3\RESULTS_DEF\single_files"

ONLY_ALL_REQUISUTES = False


# %%  

# another approach (alternative to the following code):
    
# 1. select a song
# 2.make a dictionary where for each emotion save a dictionary for all the augmentations (all users) and user ID maybe

# example:
#results = {
#    'Aggressive': { 'aug_1':[], 'aug_2':[], 'aug_3': [], ...},
#    'Relaxed': {},
#    'Happy': {},
#    'Sad': {}   
#    }

# %%


'''------------------ 1 ------------------'''
'''plot each emotion for each song separately'''

#emotions_each_augmentation = {
#    'aug_1': [  [-3, 3, 0, 1] ,  [-2, 3, 1, 0] , ... ]  -> one list for each user
#    'aug_2': []
#    'aug_3': []
#    }


# define a song name
name = 'sad2_'  # how to do with only aggressive, without the 2?

# dictionary
emotions_each_augmentation = {augmentation: [] for augmentation in AUGMENTATIONS}

# get all the paths
if ONLY_ALL_REQUISUTES:
    path_list = glob.glob(os.path.join(root_path, '*_.csv'))
else:
    path_list = glob.glob(os.path.join(root_path, '*.csv'))


# for each csv file do
for path in path_list:
    
    # open csv file
    df = pd.read_csv(path)
    
    # loop through all the augmentations
    for augmentation in AUGMENTATIONS:    
    
        # search for the emotion values for the specific row
        matching_row = df[df['Song'].str.contains(name) & df['Song'].str.contains(augmentation, na=False)]

        # Debug: Print path and matching row details
        print(f"Processing file: {path}")
        print(f"Augmentation: {augmentation}")
        print(matching_row)
        
        # get
        if not matching_row.empty:
            emotions = matching_row[['Aggressive', 'Relaxed', 'Happy', 'Sad']].values.flatten().tolist()
            emotions_each_augmentation[augmentation].append(emotions)
            print("Extracted emotions:", emotions)
            print('\n\n')
            
        else:
            print("No matching row found.")

# %%
# -------------------------------------------------------
# select emotion
#emotion = 'Aggressive'


AUGMENTATIONS = ['original', 'pitch_shift_low', 'pitch_shift_high', 'time_stretch_low', 'time_stretch_high', 'noise_addition', 'reverb','saturation', 'low_pass','high_pass', 'compressor', 'resampling']
EMOTIONS = ['Aggressive', 'Relaxed', 'Happy', 'Sad']


#save all the values for each user in a list
def get_augmentaions_for_single_emotion(emotion):
    
    emotion_index = EMOTIONS.index(emotion)
    emotion_data_per_augmentation = {augmentation: [] for augmentation in AUGMENTATIONS}
    
    for augmentation in AUGMENTATIONS:    
        for user in range(len(path_list)):
            # get value of selected emotion for each user
            emotion_value = emotions_each_augmentation[augmentation][user][emotion_index]        
            emotion_data_per_augmentation[augmentation].append(emotion_value)    
    return emotion_data_per_augmentation

# for a specific emotion get all the values of all the users (for the specific song)
emotion_data_agg = get_augmentaions_for_single_emotion('Aggressive')
emotion_data_rel = get_augmentaions_for_single_emotion('Relaxed')
emotion_data_hap = get_augmentaions_for_single_emotion('Happy')
emotion_data_sad = get_augmentaions_for_single_emotion('Sad')

# get the mean
mean_agg = [np.mean(emotion_data_agg[aug]) for aug in AUGMENTATIONS]
mean_rel = [np.mean(emotion_data_rel[aug]) for aug in AUGMENTATIONS]
mean_hap = [np.mean(emotion_data_hap[aug]) for aug in AUGMENTATIONS]
mean_sad = [np.mean(emotion_data_sad[aug]) for aug in AUGMENTATIONS]

# plot

# define bar width and positions for groups
bar_width = 0.2
x = np.arange(len(AUGMENTATIONS))

# create a plot
plt.figure(figsize=(13, 6))

# plot each emotion's bar with an offsett for each group
plt.bar(x - 1.5 * bar_width, mean_agg, width=bar_width, label='Aggressive', color='#FF6F61')
plt.bar(x - 0.5 * bar_width, mean_rel, width=bar_width, label='Relaxed', color='#6B8E23')
plt.bar(x + 0.5 * bar_width, mean_hap, width=bar_width, label='Happy', color='#F9A825')
plt.bar(x + 1.5 * bar_width, mean_sad, width=bar_width, label='Sad', color='#3F51B5')

plt.xlabel('Augmentations', fontsize=12)
plt.ylabel('Mean Emotion Value', fontsize=12)
plt.title(f'Mean Emotion Values Across Augmentations - song: {name[:-1]}', fontsize=14)
plt.xticks(x, AUGMENTATIONS, rotation=45, ha='right')
plt.ylim(-3, 3)

plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

for i in range(1, len(AUGMENTATIONS)):
    plt.axvline(x=i - 0.5, color='blue', linestyle='-', linewidth=0.7, alpha=0.4)

#plt.legend(title='Emotions')
plt.legend(title='Emotions', bbox_to_anchor=(1.00, 1), loc='upper left')


plt.tight_layout()
plt.show()

'''
plot mean and std - plot boxplot

# get the mean and std
#mean = [np.mean(emotion_data_per_augmentation[aug]) for aug in AUGMENTATIONS]
#std = [np.std(emotion_data_per_augmentation[aug]) for aug in AUGMENTATIONS]
#boxplot_data = [emotion_data_per_augmentation[aug] for aug in AUGMENTATIONS]
    
# Plot the results with error bars representing the standard deviation
plt.figure(figsize=(12, 6))
plt.bar(AUGMENTATIONS, mean, yerr=std, capsize=5, color='skyblue', edgecolor='black')
plt.xlabel('Augmentations', fontsize=12)
plt.ylabel(f'Mean {emotion} Value', fontsize=12)
plt.title(f'Mean {emotion} Across Augmentations with Standard Deviation', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(data=boxplot_data)
plt.xticks(np.arange(len(AUGMENTATIONS)), AUGMENTATIONS, rotation=45, ha='right')
plt.xlabel('Augmentations', fontsize=12)
plt.ylabel(f'{emotion} Value', fontsize=12)
plt.title(f'Distribution of {emotion} Across Augmentations', fontsize=14)

# Adjust layout to fit labels
plt.tight_layout()
plt.show()

'''
# if i want to plot all of the 4 emotions in the same plot





# %%

import numpy as np
import pandas as pd
from autorank import autorank, create_report, plot_stats


for aug in AUGMENTATIONS:
    print("Current aug:", aug)

# structure data to be used by autorank
data = pd.DataFrame({aug: emotion_data_per_augmentation[aug] for aug in AUGMENTATIONS})

# use autorank
result = autorank(data, alpha=0.05, verbose=False)

# print statistical report
print(create_report(result))

# plot stats
plot_stats(result, allow_insignificant=True)

for aug, values in emotion_data_per_augmentation.items():
    print(f'Augmentation: {aug}, Values: {values}')
    print(f'Mean: {np.mean(values)}, Median: {np.median(values)}, Std: {np.std(values)}, Unique Values: {np.unique(values)}')

## fino qui riscritto ---------------------------------------


# %%

# gpt code to plot
def plot_hist_all_augmentations(data, max_freq=32):
    num_columns = data.shape[1]
    nrows, ncols = 3, 4
    
    # Create a figure for the histograms
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 10))
    
    # Flatten axes for easier iteration
    axes = axes.flatten()
    
    # Define the bin edges for integers from -3 to 3
    bins = range(-3, 5)  # Inclusive of -3 to +3
    
    # Plot histograms for each column
    for i, column in enumerate(data.columns):
        axes[i].hist(data[column], bins=bins, color='skyblue', edgecolor='black', align='left')
        axes[i].set_title(column)
        axes[i].set_xticks(range(-3, 4))  # Ensure only integer ticks are shown
        axes[i].set_xlabel('Value')
        axes[i].set_ylabel('Frequency')
        axes[i].set_ylim(0, max_freq)
    
    # Hide unused subplots if any
    for j in range(len(data.columns), len(axes)):
        axes[j].axis('off')
    
    # Adjust layout for clarity
    plt.tight_layout()
    plt.show()


plot_hist_all_augmentations(data, 12)
# -------------------------------------------------------
# %%
# gpt code

from scipy.stats import friedmanchisquare
import scikit_posthocs as sp
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Selected emotion for analysis
selected_emotion = 'Sad'

# Prepare the data: Rows are participants, columns are augmentations
data = []
for user_idx in range(len(path_list)):  # Loop over participants
    row = [emotions_each_augmentation[aug][user_idx][EMOTIONS.index(selected_emotion)]
           for aug in AUGMENTATIONS]
    data.append(row)

# Convert to numpy array for analysis
data_array = np.array(data)  # Shape: (num_participants, num_augmentations)

# ---

# Perform Friedman test
stat, p_value = friedmanchisquare(*data_array.T)  # Transpose to have columns as augmentations

print(f"Friedman Test Statistic: {stat}")
print(f"P-value: {p_value}")

if p_value < 0.05:
    print("Significant differences found among the augmentations.")
else:
    print("No significant differences among the augmentations.")

# ---

# Perform Nemenyi post-hoc test
posthoc_results = sp.posthoc_nemenyi_friedman(data_array)

# Display pairwise comparison results
print(posthoc_results)

# Visualize results with a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(posthoc_results, annot=True, fmt=".3f", xticklabels=AUGMENTATIONS, yticklabels=AUGMENTATIONS, cmap="coolwarm")
plt.title(f"Nemenyi Post-Hoc Test Results for {selected_emotion}")
plt.show()

# ---
# %%

'''------------------ 2 ------------------'''
'''put together all the songs and plot each emotin separately'''

# for each emotion* do

# for each augmentation

# find the current emotion value (e.g., 'Sad') for all the songs with the specific augmentation

# ---------

AUGMENTATIONS = ['original', 'pitch_shift_low', 'pitch_shift_high', 'time_stretch_low', 'time_stretch_high', 'noise_addition', 'reverb','saturation', 'low_pass','high_pass', 'compressor', 'resampling']
EMOTIONS = ['Aggressive', 'Relaxed', 'Happy', 'Sad']

# dict to save resuts
all_songs = { emotion: {} for emotion in EMOTIONS}
for emotion in EMOTIONS:
    for augmentation in AUGMENTATIONS:
        all_songs[emotion][augmentation] = []


# get all file paths
path_list = glob.glob(os.path.join(rooth_path, '*.csv'))

# for each csv file do
for path in path_list:
    
    # open csv file
    df = pd.read_csv(path)
    
    # consider each emotion separately
    for emotion in EMOTIONS:
        
        
        # consider a specific augmentation
        for augmentation in AUGMENTATIONS:
            
            # find all the file names with that augmentation          
            matching_rows = df[df['Song'].str.contains(augmentation, na=False)]
            
            # take only the value for the specific emotion
            emotion_list = matching_rows[emotion].values.flatten().tolist()
            
            # save results in dictionary
            all_songs[emotion][augmentation].extend(emotion_list)
            
# %%
# plot!
emotion = 'Aggressive'


mean_values = []
std_values = []

for augmentation in AUGMENTATIONS:
    
    emotion_values = all_songs[emotion][augmentation]
        
    mean_values.append(np.mean(emotion_values))
    std_values.append(np.std(emotion_values))
    


# Plot the results with error bars representing the standard deviation
plt.figure(figsize=(12, 6))
#plt.bar(AUGMENTATIONS, mean_values, yerr=std_values, capsize=5, color='skyblue', edgecolor='black')
plt.bar(AUGMENTATIONS, mean_values, capsize=5, color='skyblue', edgecolor='black')
plt.xlabel('Augmentations', fontsize=12)
plt.ylabel(f'Mean {emotion} Value', fontsize=12)
plt.title(f'Mean {emotion} Across Augmentations with Standard Deviation', fontsize=14)
plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for readability
plt.tight_layout()  # Ensure everything fits nicely in the plot
plt.show()  





# %%




# --------------------------------------------------

# verify: code by chatgpt

import numpy as np
import pandas as pd
from autorank import autorank, create_report, plot_stats

AUGMENTATIONS = ['original', 'pitch_shift_low', 'pitch_shift_high', 'time_stretch_low', 'time_stretch_high', 'noise_addition', 'reverb','saturation', 'low_pass','high_pass', 'compressor', 'resampling']

# Select emotion
selected_emotion = "Aggressive"


# Prepare the data as a DataFrame

# i could also use: data = pd.DataFrame(all_songs[selected_emotion])
data = pd.DataFrame({augmentation: all_songs[selected_emotion][augmentation] for augmentation in AUGMENTATIONS})

# Use autorank to analyze differences
result = autorank(data, alpha=0.05, verbose=False)


# Print the statistical report
print(create_report(result))

print(result)

# Plot the statistical summary
#plot_stats(result)
plot_stats(result, allow_insignificant=True)


# ricontrolla c'è qualcosa che non torna con questi plot forse
plot_hist_all_augmentations(data, max_freq=45)

# %%

        

# - - - - - - - - - - - - - -
# - - - - - - - - - - - - - -
# - - - - - - - - - - - - - -

'''in this code i want to compare the results for a single song among all the 4 emotions'''

# GPT code to verify unique files
def verify_uniqueness_song_names(path_temp):
    
    # get csv file
    df_temp = pd.read_csv(path_temp)
    
    # Extract the 'Song' column as a list
    song_list = df_temp["Song"].tolist()
    
    # Check for uniqueness by comparing list length with set length
    unique_values = len(song_list) == len(set(song_list))
    
    # Print the result
    if unique_values:
        print("The 'Song' column contains unique values only.")
    else:
        print("The 'Song' column contains duplicate values.")

# get list of all the paths in RESULTS_DEF
path_list = glob.glob(os.path.join(rooth_path, '*.csv'))

# verify uniqueness of the values in "Song" column
for path in path_list: verify_uniqueness_song_names(path)



# verify mean vote across all csv files of song 1 (use \\ for some reason)
song_name1 = "augmented\\0__original\\0__aggressive2_original_then.wav"
song_name2 = "augmented\\5__aggressive\\aggressive2_low_pass.wav"
song_name3 = "augmented\\5__aggressive\\aggressive2_pitch_shift_low.wav"
song_name4 = "augmented\\5__aggressive\\aggressive2_saturation.wav"



# get the evaluation of song for the 4 emotions - all csv files - (same for song2)

def get_results_single_song(song_name, path_list):
    
    # create empty dictionary
    results = {}
    
    for path in path_list:
        
        # get csv file
        df = pd.read_csv(path)
        
        # get values for a specific song
        filtered_row = df[df['Song'] == song_name]
        
        # retrieve values in a list
        if not filtered_row.empty:
            emotion_list = filtered_row[['Aggressive', 'Relaxed', 'Happy', 'Sad']].iloc[0].tolist()
            results[path] = emotion_list
    return results

results_song_1 = get_results_single_song(song_name1, path_list)
results_song_2 = get_results_single_song(song_name2, path_list)
results_song_3 = get_results_single_song(song_name3, path_list)
results_song_4 = get_results_single_song(song_name4, path_list)    

import numpy as np
# now I want to compare the results

def get_mean_value(results_song):
    total = np.array([0, 0, 0, 0])
    for list_emotions in results_song.values():
        total += np.array(list_emotions)
    return total / len(results_song)

    
mean_1 = get_mean_value(results_song_1)
mean_2 = get_mean_value(results_song_2)
mean_3 = get_mean_value(results_song_3)
mean_4 = get_mean_value(results_song_4)


   

# - - - - - - - - - - - - - -
# - - - - - - - - - - - - - -
# - - - - - - - - - - - - - -

'''consider only two csv files (part1 and part2 of a single user)'''
'''*consider make the same with more csv files and then compare the mean values'''

from pprint import pprint

df = pd.read_csv(path1) 
df2 = pd.read_csv(path2)


results = {}

for emotion in EMOTIONS:
    
    # create empty dictionry
    results[emotion] = {}
    
    for augmentation in AUGMENTATIONS:
        
        # filter rows where "Song" contains the specific augmentation (case-insensitive)
        filtered_df = df[df['Song'].str.contains(augmentation, case=False, na=False)]
        filtered_df2 = df2[df2['Song'].str.contains(augmentation, case=False, na=False)]
            
        # extract the values fo the specific emotion and save it into a list
        emotion_list = filtered_df[emotion].tolist() + filtered_df2[emotion].tolist()

        # save result in a dictionry    
        results[emotion][augmentation] = emotion_list
pprint(results, sort_dicts=False)

# - - - - - - - - - - - - - -
# - - - - - - - - - - - - - -
# - - - - - - - - - - - - - -

# display the man value for each augmentation of a specific emotion e.g. Aggressive
import matplotlib.pyplot as plt
import numpy as np

selected_emotion = "Relaxed"

# get dictionry of specific emotion
emotion_data = results[selected_emotion]

# get labels and mean values
augmentations = list(emotion_data.keys())
mean_values = [np.median(values) for values in emotion_data.values()]

# plot
#plt.title(f'Average {selected_emotion} Values Across Augmentations')
plt.figure(figsize=(8, 5))
plt.xlabel('Augmentations')
plt.ylabel(f'{selected_emotion} Value')

plt.bar(augmentations, mean_values)
#plt.barh(augmentations, mean_values, color='skyblue')
#plt.plot(augmentations, mean_values, marker='o', linestyle='-', color='skyblue')


#plt.ylim(-1.75, -0.50)

plt.xticks(rotation=90)
plt.show()

# - - - - - - - - - - - - - -
# - - - - - - - - - - - - - -
# - - - - - - - - - - - - - -

# make statistical test

# 1. I want to see for a specific emotion (e.g., Aggressive) 
# if original is stat. different from an augmentation (e.g., Saturation)

import numpy as np
from scipy import stats

selected_emotion = "Aggressive"

# get the aggressive values for original
a = results[selected_emotion]['original']
b = results[selected_emotion]['resampling']


t_stat, p_value = stats.ttest_ind(a, b, equal_var=False)

# for dependent populations which is my case now
t_stat2, p_value2 = stats.ttest_rel(a, b)

print(f'T-statistic: {t_stat}')
print(f'P-value: {p_value}')

print(f'T-statistic2: {t_stat2}')
print(f'P-value2: {p_value2}')











