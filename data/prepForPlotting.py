# -*- coding: utf-8 -*-
"""
Title: prepForPlotting.py

This program prepares the song matches for plotting.  It takes the matched
song times and calculates what percent of the film has elapsed by the time the
song begins and ends (ex: song 1 starts 2% into the total runtime and ends 
after 3.5% of the film has played).

Input:
disney_animated_feature_films.csv
final_matches.csv (output from getSongTimes.py)

Output:
final_matches.csv

Created on Sat Feb 18 13:38:19 2017

@author: Alice
"""
import pandas as pd

disney_films = pd.read_csv('disney_animated_feature_films.csv')
song_times = pd.read_csv('final_matches.csv')
    
# add on runtimes to song_times
film_lengths = disney_films[['Film Number', 'Title', 'Runtime']]

final_output = song_times.merge(film_lengths, left_on='Film', right_on='Title')

# convert runtimes to seconds
final_output['Runtime_Seconds'] = pd.to_numeric(final_output['Runtime'].str.split().str[0])*60

# calculate percent of the film that has elapsed before each song begins and ends
final_output['Start_pos'] = (pd.to_datetime(final_output.Start_time, format='%H:%M:%S,%f').dt.hour*3600 + 
                             pd.to_datetime(final_output.Start_time, format='%H:%M:%S,%f').dt.minute*60 + 
                             pd.to_datetime(final_output.Start_time, format='%H:%M:%S,%f').dt.second)/final_output['Runtime_Seconds']
final_output['End_pos'] = (pd.to_datetime(final_output.End_time, format='%H:%M:%S,%f').dt.hour*3600 + 
                           pd.to_datetime(final_output.End_time, format='%H:%M:%S,%f').dt.minute*60 + 
                           pd.to_datetime(final_output.End_time, format='%H:%M:%S,%f').dt.second)/final_output['Runtime_Seconds']

# write out final dataset for plotting
final_output.to_csv('final_matches.csv', index=False)