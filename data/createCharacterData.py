# -*- coding: utf-8 -*-
"""
Title: createCharacterData.py

This program creates all additional support datasets needed including:
- a dataset with all of the unique character names that have singing roles 
in Disney animated feature films.  Extra attributes (gender, protagonist 
status) about the characters will be added manually
- a dataset with the names of the characters that have a part in each song and
their gender and protagonist status added on

Input: song_lyrics.csv
Output: character_data.csv, characters_by_song.csv

Created on Mon Jan 23 19:22:49 2017

@author: Alice
"""

import pandas as pd

lyrics_data = pd.read_csv("song_lyrics.csv")

# create a list of all characters who have a singing role per film
all_characters = lyrics_data[["Film", "Character"]]
all_characters = all_characters.drop_duplicates()
all_characters.to_csv("character_data2.csv", index=False) # manually add gender and hero/villain status to this file

# create a list of all unique characters who sing per song
characters_by_song = lyrics_data[["Film", "Song_Title", "Character"]]
characters_by_song = characters_by_song.drop_duplicates()

# add on gender and hero/villain status to each character
character_data = pd.read_csv("character_data.csv")
characters = characters_by_song.merge(character_data, on=["Film", "Character"])
characters.sort_values(by=['Film', 'Song_Title'], inplace=True)

characters.to_csv("characters_by_song2.csv", index=False)

