# Author Conor O'Kelly

"""
This file will contain all the functions that are required to fetch the extra data stored on external websites.
"""

import urllib.request as request
import json
import re
#import api_keys.py

# Will also have all data required from rotton tomamtoes
# The imdb database api. Take name of movie and return info from imdb

def imdb_data_call(movie):

    movie = "Mad Max: Fury Road"

    movie = movie.replace(" ", "+").replace(":","%3A") # Format move name input

    # request url
    url = "http://www.omdbapi.com/?t="+movie+"=&plot=short&r=json&tomatoes=true"

    #Request and get json file
    current_json_file = request.urlopen(url).read()

    # Error handling if movie not found

    # Convert file to UTF-8
    current_json_file = current_json_file.decode("UTF-8")

    # Convert each station to a list of dicts
    move_data = json.loads(current_json_file)

    # Format awards for data set
    awards = move_data.get("Awards")
    print(awards)
    if len(awards) > 5:
        oscars = re.search("Won\s\d{1,2}\sOscar",awards).group().split(" ")[1] # Find string. Return match. Split on spaces. List item 1
        wins = re.search("\s\d{1,4}\swin", awards).group().split(" ")[1]
        nominations = re.search("\s\d{1,4}\snomination", awards).group().split(" ")[1]
    else:
        oscars = 0
        wins = 0
        nominations = 0
    print(oscars,wins,nominations)


    # Selecte dub dict
    new_move_dict = {"Title":move_data.get("Title"),
                     "Runtime":move_data.get("Runtime"),
                     "imdbID":move_data.get("imdbID"),
                     "Title":move_data.get("Title"),
                     "Director":move_data.get("Director"),
                     "Released":move_data.get("Released"),
                     "imdbRating":move_data.get("imdbRating"),
                     "Metascore":move_data.get("Metascore"),
                     "Rated":move_data.get("Rated"),
                     "Metascore":move_data.get("Metascore"),
                     "Genre":move_data.get("Genre"),
                     #Formated awards
                     "Awards":move_data.get("Awards"),
                     # Rotton tomatoes Data - Ratings
                     "tCriticScore":move_data.get("tomatoUserMeter"),
                     "tUserScore":move_data.get("tomatoMeter"),
                     # Rotton tomatoes Data - No of Reviews
                     "tNoUsers":move_data.get("tomatoUserReviews"),
                     "tNoCritics":move_data.get("tomatoReviews"),
                     # Rotton tomatoes Data - Avg review
                     "tUserAverage":move_data.get("tomatoUserRating"),
                     "tCriticAverage":move_data.get("tomatoRating"),
                     }

    return new_move_dict

if __name__ == '__main__':
    x =imdb_data_call(1)

