# -*- coding: utf-8 -*-
"""
Title: getSongTimes.py

This program takes the subtitle datasets generated by createSubsData.py
for each Disney feature animation and matches each line against lyrics
from songs in that film to determine the start and end time of every song.  

Inputs:
animated_list.csv
song_lyrics.csv
subtitle files for each film (in a subdirectory named 'subs')

Output:
final_matches.csv

Date Created: Oct. 30, 2016

Author: Alice Feng
"""

import os
import pandas as pd
import numpy as np
import string
import datetime

def minimize_subdata(film):
    """ Reduces the subtitle dataset if possible to minimize the number of 
    lines that must be compared.  For subtitles that specially mark sung lines,
    it will only return those subtitle lines for comparison.
    
    Args:
        film: the name of the film as a String
        
    Returns:
        subdata: a dataframe with only the sung lines from the subtitle if 
                 possible, otherwise returns all of the subtitles
    """
    
    data = pd.read_csv(os.path.join('subs', film + '.csv'))

    if film in ['Pinocchio', 'Bambi', 'The Aristocats']:
        subdata = data.loc[data.text.str.contains("♪", na=False)]
    elif film in ['Cinderella']:
        subdata = data.loc[data.text.str.contains("<i>", na=False)]
    elif film in ['Alice in Wonderland']:
        subdata = data.loc[data.text.str.contains("♫", na=False)]
    elif film in ['The Sword in the Stone']:
        subdata = data.loc[data.text.str.contains("%%", na=False)]
    else:
        subdata = data
    
    # reset index so we can iterate through the dataframe using a counter
    return subdata
                

# write a line matching function
def line_match(sub_line, lyric_line):
    """ Attempts to match subtitle lines to lyric lines to identify the song
    sung.
    
    It uses probabilistic matching based on the number of matching words and 
    order of words between the two sources.  Lines that match exactly or are
    a perfect subset of the other return a probability of 1 of being a match.
    
    Lines that do not match perfectly as-is are then split into a bag of words
    and the number of words from the subtitle and lyric bags found in both are
    counted.  The ratio of the number of words found in both to the total 
    number of words in the shorter of the two lines is returned as the 
    probability of being match.
    
    Args:
        sub_line: one line of text from the subtitle file
        lyric_line: one line of lyrics
        
    Returns:
        a float between 0 - 1 that is the probability of the subtitle and lyric
        being a match    
    """
    # first clean the lines
    sub_clean = sub_line.replace("<i>", "").replace("</i>", "").lower().translate(string.maketrans("",""), string.punctuation).strip("♪").strip("♫").strip()
    lyric_clean = lyric_line.lower().translate(string.maketrans("",""), string.punctuation)
    
    # calculate probability of a match between subtitle and lyric lines
    if sub_clean == lyric_clean:
        return 1
    elif (sub_clean in lyric_clean) or (lyric_clean in sub_clean):
        return 1
    else:
        sub_words = sub_clean.split()
        lyric_words = lyric_clean.split()
        common = list(set(sub_words) & set(lyric_words))
       
        if len(common) == len(sub_words) or len(common) == len(lyric_words):
            return 0  # don't count as a match if all of the words match but aren't in the same order
        elif len(sub_words) < len(lyric_words):
            return float(len(common))/len(sub_words)
        else:
            return float(len(common))/len(lyric_words)
   
    
    
    
# read in data
disney_films = pd.read_csv('disney_animated_feature_films.csv')
song_lyrics = pd.read_csv('song_lyrics.csv')
    
films = ['Snow White and the Seven Dwarfs', 'Pinocchio']
match = []
    
for film in films:
    subdata = minimize_subdata(film)    
    lyricdata = song_lyrics[song_lyrics.Film == film]
        
    # try matching each line in the subs with a line from any of the songs
    for i in subdata.index:
        for j in lyricdata.index:
            # only match on lines with more than 2 words to reduce false positives
            if len(subdata.text[i].split()) > 2 and len(lyricdata.Lyric[j].split()) > 2:
                match_prob = line_match(subdata.text[i], lyricdata.Lyric[j])
                # lines with > 80% probability of being a match are considered
                # to be a match                
                if match_prob > 0.8:
                    match.append({'Film': film,
                                  'Sub_no': subdata.sub_no[i], 
                                  'Subtitle': subdata.text[i],
                                  'Lyric': lyricdata.Lyric[j],
                                  'Lyric_num': lyricdata.Line_num[j],
                                  'Song': lyricdata.Song_Title[j],
                                  'Start_time': subdata.start_time[i],
                                  'End_time': subdata.end_time[i]}) 
    
    # create a dataframe of all found matches 
    match_df = pd.DataFrame(match, columns=['Film', 'Sub_no', 'Subtitle', 'Lyric', 'Lyric_num', 'match_prob',
                                            'Song', 'Start_time', 'End_time'])
    
    # sort dataset by film, start time, and lyric number matched to
    match_df.sort_values(by=['Film', 'Start_time', 'Lyric_num'], inplace=True)
    match_df.index = range(1, len(match_df) + 1)
    
    # calculate how much time has elapsed between lines   
    match_df.loc[:, 'Prev_end_time'] = match_df['End_time'].shift(1)
    match_df.loc[:, 'Time_diff'] = (pd.to_datetime(match_df.Start_time, format='%H:%M:%S,%f') - pd.to_datetime(match_df.Prev_end_time, format='%H:%M:%S,%f'))/np.timedelta64(1, 's')
    
    # add a song number to each song in order of appearance to catch reprises
    match_df.loc[:, 'Song_num'] = 1
    for i in range(2, len(match_df) + 1):
        # restart the song number for each movie        
        if match_df['Film'][i] != match_df['Film'][i-1]:
            match_df['Song_num'][i] = 1
        # if the song title is the same but there's been too long of a gap 
        # between current and previous line and the current line matches a lyric
        # that occurs prior to the previous line's match, treat as a new song (reprise)
        elif match_df['Time_diff'][i] > 60 and (match_df['Lyric_num'][i] - match_df['Lyric_num'][i-1]) < 0:
            match_df['Song_num'][i] = match_df['Song_num'][i-1] + 1
        # new song number when the song name changes
        elif match_df['Song'][i] != match_df['Song'][i-1]:
            match_df['Song_num'][i] = match_df['Song_num'][i-1] + 1
        else:
            match_df['Song_num'][i] = match_df['Song_num'][i-1]

                                            
    # get start and end times of each song
    song_times = match_df.groupby(by=['Film', 'Song', 'Song_num'], 
                                  as_index=False).agg({'Start_time': min, 'End_time': max})
    
    # calculate length of each song
    song_times['Length'] = pd.to_datetime(song_times.End_time, format='%H:%M:%S,%f') - pd.to_datetime(song_times.Start_time, format='%H:%M:%S,%f')
    
    # sort song_times by film and song start time
    song_times.sort_values(by=['Film', 'Start_time'], inplace=True)
    
    # remove "songs" with length of less than 10 sec
    song_times = song_times[song_times.Length > datetime.timedelta(seconds=10)]
    
    
### Prep dataset for plotting
    
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

# write out final output
final_output.to_csv('final_matches.csv', index=False)
