# -*- coding: utf-8 -*-
"""
Title: makeViz.py

This program sketches the basis for the final visualization.  It uses the
matched data to draw lines proportional to each film's length, then adds 
markings representing where each song starts and ends during the film's 
runtime.

Input:
disney_animated_feature_films.csv
final_matches_clean.csv (output from prepForPlotting.py copied over)

Output:
sketch.pdf

Created on Wed Jan 25 21:14:57 2017

@author: Alice
"""

from pyx import *
import pandas as pd

disney_films = pd.read_csv('data\\disney_animated_feature_films.csv')
films = disney_films[disney_films['Include?'] == 'Y']
films.index = range(len(films))
films = films[['Film Number', 'Title', 'Runtime']]
films['Runtime'] = pd.to_numeric(films['Runtime'].str.split().str[0])

final_matches = pd.read_csv('data\\final_matches_clean.csv')

# try drawing some lines
unit.set(defaultunit='cm')
c = canvas.canvas()

for i in range(len(films)):
    film = films['Title'][i]
    #c.text(0, i, r"test")  # how to add text? - need to install LaTeX
    x2 = (25.0/max(films['Runtime']))*films['Runtime'][i]
    c.stroke(path.line(0, i, x2, i))

    try:
        match_data = final_matches[final_matches.Film == film]
        for j in match_data.index:
            start = match_data.Start_pos[j] * x2
            end = match_data.End_pos[j] * x2
            song = path.path(path.moveto(start, i-0.25), path.lineto(start, i+0.5),
                             path.lineto(end, i+0.5), path.lineto(end, i-0.25))
            c.stroke(song)
    except:
        continue

c.writePDFfile("sketch1")