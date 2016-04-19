# Author Conor O'Kelly

"""
This file will contain all the functions that are required to fetch the extra data stored on external websites.
"""

import json
import re
import urllib.request as request

from info_requests.meta_critic_web_scraper import retieve_person_score


# Will also have all data required from rotton tomamtoes
# The imdb database api. Take name of movie and return info from imdb

def imdb_data_call(movie):

    search_movie = movie.replace(" ", "+").replace("-", "+").replace(":","%3A") # Format move name input
    # print(search_movie)

    # request url
    url = "http://www.omdbapi.com/?t="+search_movie+"=&plot=short&r=json&tomatoes=true"

    #Request and get json file
    current_json_file = request.urlopen(url).read()

    # Error handling if movie not found

    # Convert file to UTF-8
    current_json_file = current_json_file.decode("UTF-8")

    # Convert each station to a list of dicts
    move_data = json.loads(current_json_file)

    # Test that response as positive
    if (move_data.get("Response") == "True"):
        # Format awards for data set
        awards = move_data.get("Awards")

        if len(awards) > 5:
            try:
                oscars = re.search("Won\s\d{1,2}\sOscar",awards).group().split(" ")[1] # Find string. Return match. Split on spaces. List item 1
            except:
                oscars = 0
            try:
                nom_oscars = re.search("Nominated for\s\d{1,2}\sOscar",awards).group().split(" ")[2]
            except:
                nom_oscars = 0
            try:
                wins = re.search("\s\d{1,4}\swin", awards).group().split(" ")[1]
            except:
                wins = 0
            try:
                nominations = re.search("\s\d{1,4}\snomination", awards).group().split(" ")[1]
            except:
                nominations = 0

        # Seperate out generes
        try:
            genres = move_data.get("Genre")
            genres = genres.replace(",", "").split(" ")

            # Set genres according to number of items given from dict
            if (len(genres) == 3):
                genre_1 = genres[0]
                genre_2 = genres[1]
                genre_3 = genres[2]
            elif (len(genres) == 2):
                genre_1 = genres[0]
                genre_2 = genres[1]
                genre_3 = None
            else:
                genre_1 = genres
                genre_2 = None
                genre_3 = None

            # print(genre_1,genre_2,genre_3)
        except:
            pass

        # Get director score if found.
        try:
            director_name = move_data.get("Director")
            # print(director_name)
            director_score = retieve_person_score(director_name)
            # print(director_score)
        except:
            print("Failed to find meta critic score for director " + move_data.get("Director"))
            director_score = None


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
                         # Three genre attributes
                         "Genre1":genre_1,
                         "Genre2":genre_2,
                         "Genre3":genre_3,
                         #Formated awards
                         "oscars":oscars,         # oscars,nom_oscars,wins,nominations
                         "nom_oscars":nom_oscars,
                         "wins":wins,
                         "nominations":nominations,
                         # Rotton tomatoes Data - Ratings
                         "tCriticScore":move_data.get("tomatoUserMeter"),
                         "tUserScore":move_data.get("tomatoMeter"),
                         # Rotton tomatoes Data - No of Reviews
                         "tNoUsers":move_data.get("tomatoUserReviews"),
                         "tNoCritics":move_data.get("tomatoReviews"),
                         # Rotton tomatoes Data - Avg review
                         "tUserAverage":move_data.get("tomatoUserRating"),
                         "tCriticAverage":move_data.get("tomatoRating"),
                         # Director meta critic rating
                         "directorMetaRating":director_score
                         }

        return new_move_dict

    # Else => move response not true (aka false)
    else:
        print("No response found for movie => " + movie)


if __name__ == '__main__':
    x =imdb_data_call("Mad Max: Fury Road")
    y =imdb_data_call("Jungle book")
    print(x)

