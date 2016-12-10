# -*- coding: utf-8 -*-
"""
Title: createSubsData.py

This program converts subtitle files into rectangular datasets.
Columns:
  sub_no: number order subtitle appears in the film
  start_time: when the subtitle appears onscreen
  end_time: when the subtitle ends
  text: text that is displayed onscreen
Each row corresponds to one subtitle that appears onscreen.

Inputs:
disney_animated_feature_films.csv
subtitle files for each Disney animated feature film
(Note: this program assumes your .srt files are in a subdirectory called 'subs')

Output:
a dataset for each film

Date Created: Nov. 7, 2016

Author: Alice Feng
"""

import os
import pandas as pd

def parse_start_time(line):
    """ Extracts the start time from a line with start and end times.
    
    Args:
        One subtitle line of format XX:XX:XX,XXX --> XX:XX:XX,XXX
    
    Returns:
        Start time for when the subtitle begins to appear onscreen
    """
    start = line.split('-->')[0].strip()
    return start
    
def parse_end_time(line):
    """ Extracts the end time from a line with start and end times.
    
    Args:
        One subtitle line of format XX:XX:XX,XXX --> XX:XX:XX,XXX
    
    Returns:
        End time for when the subtitle appears onscreen
    """
    end = line.split('-->')[1].strip()
    return end
    
def parse_subtitle_text(subs, linenum):
    """ Extracts all subtitle text that appear together on screen at one 
    point in time, even if the text is split across multiple lines in the 
    subtitle file.
    
    Args:
        Subtitle line(s) of text corresponding to a start/end time
        
    Returns:
        All subtitle text as one string
    """
    i = linenum + 2
    text = ''
    while subs[i] != '' and i < len(subs):
        text = text + subs[i].strip() + ' '
        i = i + 1
        if i == len(subs):  # for files that do not have blank carriage returns at the end
            break
    return text.strip()
    
    
    
# create list of films 
disney_films = pd.read_csv('disney_animated_feature_films.csv')
films = disney_films.Title[disney_films['Include?'] == 'Y']

# iterate through each film in the list and create a subtitle dataset for it
for film in films:
    filename = film + '.srt'
    
    try:
        subs_file = open(os.path.join('subs', filename))
        
        subs = subs_file.read().decode("utf-8-sig").encode("utf-8")
        subs_lines = subs.split('\n')
        
        sub_data = []
        
        # parse subtitle file
        for i in range(len(subs_lines)):
            if subs_lines[i].isdigit():
                num = subs_lines[i].strip()
                start_time = parse_start_time(subs_lines[i+1])
                end_time = parse_end_time(subs_lines[i+1])
                text = parse_subtitle_text(subs_lines, i)
                sub_data.append({'sub_no': num, 
                                 'start_time': start_time, 
                                 'end_time': end_time,
                                 'text': text})
            else:
                continue
        
        subs_file.close()
        
        # write out data as a Pandas dataframe to csv
        csv_filename = film + '.csv'
        df = pd.DataFrame(sub_data)
        df.to_csv(os.path.join('subs', csv_filename), index=False)
    except:
        print "Missing subtitles for:", film