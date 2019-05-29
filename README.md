# Introduction
Script to create the XML file to use [Strava heatmaps](https://www.strava.com/heatmap) in [Locus Map](https://www.locusmap.eu/).
The main challenge is that you need to refresh the cookie every week, as described [here](https://help.locusmap.eu/topic/strava-heatmap-requires-now-authentification-at-higher-zoom#comment-70872).

# Usage

1. First you need to get the cookies. I can no longer get it to work in Chrome, but this works in Firefox:
   1. go to https://www.strava.com/heatmap and login. 
   1. Zoom in on the map to make sure the cookie gets stored.
1. run the script `strava.py`. It creates an xml file.
1. copy to file to your phone in Locus/mapsOnline/custom
1. start locus, and it will find the new maps.




