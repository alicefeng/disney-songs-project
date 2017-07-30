# disney-songs-project
An analysis and visualization of when songs occur during Disney animated films and their attributes.

## Current Files

makeViz.py - this script uses the pyx library to automatically draw a line whose length corresponds to the length of the movie and draws the start and end of each song using the results of prepForPlotting.py. The pdf it generates is then brought into Adobe Illustrator to serve as a basis for making the final visualization.

Data subdirectory:
- createSubsData.py - this script converts subtitle files (.srt) into a usable dataset with subtitles mapped to their start and end times
- getSongTimes.py - this script tries to parse the start and end times of each song via probabilistic matching of subtitles to lyrics
- createCharacterData.py - this script builds a dataset of characters with a singing role in a Disney film and their corresponding attributes (gender, hero/villain status, importance to the plot)
- prepForPlotting.py - this script prepares the output from getSongTimes.py for plotting by calculating the start and end of each song as a percentage of the total runtime that has elapsed