# Cartographor's Report Generator

For [Agora Nomic](http://agoranomic.org).

This repository generates HTML files and (soon) text files that track
the Map of the Land of Arcadia for the Cartographor. Soon, the
collection of data from the mailing list will be automated too,
hopefully.

**WARNING**: The code contained herein may be extremely hacky, but it's
okay because it works.

Handy guide to files and folders:

- data/ - houses all of the information about the map.
- generate.py - creates an html map.
- maps/ - this is where the generated html files go.
- template.html - the template generate.py uses to make html maps.