# disney-songs-project
An analysis and visualization of when songs occur during Disney animated films and their attributes.

## Current Files

Data subdirectory:
- createSubsData.py - this script converts subtitle files (.srt) into a usable dataset with subtitles mapped to their start and end times
- getSongTimes.py - this script tries to parse the start and end times of each song via probabilistic matching of subtitles to lyrics
