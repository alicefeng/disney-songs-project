# -*- coding: utf-8 -*-
"""
Title: createSubsData.py

This program converts subtitle files into rectangular datasets.
Columns:
  sub_no: order subtitle appears in the film
  start_time: when the subtitle appears
  end_time: when the subtitle ends
  text: text that is displayed onscreen
Each row corresponds to one subtitle that appears onscreen.

Inputs:
subtitle files for each Disney animated feature film
(Note: this program assumes your .srt files are in a subdirectory called 'subs')

Output:
a dataset for each film

Date Created: Nov. 7, 2016

Author: Alice Feng
"""

import os
import pandas as pd

# define some functions:
 
# gets the start time from a line with times
def parse_start_time(line):
    start = line.split('-->')[0].strip()
    return start
    
# gets the end time from a line with times
def parse_end_time(line):
    end = line.split('-->')[1].strip()
    return end
    
# gets all subtitle text that appear on screen (even if split across lines)
def parse_subtitle_text(subs, linenum):
    i = linenum + 2
    text = ''
    while subs[i] != '' and i < len(subs):
        text = text + subs[i].strip() + ' '
        i = i + 1
        if i == len(subs):
            break
    return text.strip()
    
    
    
# read in data
film = 'Dumbo'  # change film name here
filename = film + '.srt'

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

# write out data
csv_filename = film + '.csv'
df = pd.DataFrame(sub_data)
df.to_csv(csv_filename, index=False)