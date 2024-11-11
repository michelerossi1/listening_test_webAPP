# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 08:28:06 2024

@author: miche
"""

import pandas as pd

AUGMENTATIONS = ['original', 'pitch_shift_low', 'pitch_shift_high', 'time_stretch_low', 'time_stretch_high', 'noise_addition', 'reverb','saturation', 'low_pass','high_pass', 'compressor', 'resampling']
EMOTIONS = ['Aggressive', 'Relaxed', 'Happy', 'Sad']


path1 = 'Luca Turchet_42_07nov2024_09-17am_part1.csv'
path2 = 'Luca Turchet_42_07nov2024_09-17am_part2.csv'

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

# - - - - - - - - - - - - - -
# - - - - - - - - - - - - - -
# - - - - - - - - - - - - - -

# display the man value for each augmentation of a specific emotion e.g. Aggressive
import matplotlib.pyplot as plt
import numpy as np

selected_emotion = "Sad"

# get dictionry of specific emotion
emotion_data = results[selected_emotion]

# get labels and mean values
augmentations = list(emotion_data.keys())
mean_values = [np.mean(values) for values in emotion_data.values()]

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

selected_emotion = "Sad"

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











