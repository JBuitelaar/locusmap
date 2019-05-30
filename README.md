# Introduction
Script to create the XML file to use [Strava heatmaps](https://www.strava.com/heatmap) in [Locus Map](https://www.locusmap.eu/).
The main challenge is that you need to refresh the cookie every week, as described [here](https://help.locusmap.eu/topic/strava-heatmap-requires-now-authentification-at-higher-zoom#comment-70872).

# Usage
1. enter your login details in strava_login.json
1. run the script `strava.py`. It creates an xml file.
1. copy to file to your phone in Locus/mapsOnline/custom
1. start locus, and it will find the new maps.

It uses a trick described [here](https://github.com/nnngrach/strava_auto_auth). Alternatively, you can
get the cookies from a browser. For that you need to go to https://www.strava.com/heatmap and login. 
Next zoom in on the map to make sure the cookie gets stored. I can no longer get it to work in Chrome, but this 
works in Firefox. After that, you can use the method `get_cookies_from_browser` to create the cookie string.
See the commented out code.



