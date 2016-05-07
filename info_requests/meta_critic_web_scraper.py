# Author Conor O'Kelly

"""
This package will attempted to take the name of a director from the IMDB api.
This will the return the average career score of that director.
"""

from bs4 import BeautifulSoup
import urllib.request as request
import urllib
import re
import unicodedata

class MetaCriticRequestFailed(Exception):

    def __init__(self,actor_name):
        self.actor_name = actor_name
    def __repr__(self):
        return "Failed meta critic request for actor name " + self.actor_name

def retieve_person_score(search_name):

    # Format search term
    search_name_formated = search_name.lower().replace(" ", "-").replace(".","")
    normalise_name = str(unicodedata.normalize('NFKD', search_name_formated).encode('ascii','ignore'))
    strip_encoding = normalise_name[1:].replace("'","")



    # Create request url
    request_url = "http://www.metacritic.com/person/" + strip_encoding
    # print(request_url)

    # Format request with headers to spoof server
    req = request.Request(
    request_url,
    data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    # Do request and catch any errors
    try:
        html_page = request.urlopen(req)

        cleaned_html = BeautifulSoup(html_page,"html.parser")
        average_reviews_section = cleaned_html.find("tr", {"class": "review_average"}).getText() # Find correct div and retrun only text

        try:
            score = re.search("\d{1,2}",average_reviews_section).group()
        except:
            score = None
        # print(average_reviews_section)
        # print(score)

        return score

    except urllib.error.HTTPError as err:
        if err.code == 404:
            # print("404 page not found errror for search term => " + search_name)
            pass
        else:
            print(err.code + "error for search term => " + search_name)
        return 0

    except:
        return 0
        pass
        # raise MetaCriticRequestFailed(search_name)


if __name__ == '__main__':
    print("Start")
    x = retieve_person_score("Stellan Skarsgård")
    # y = retieve_person_score('Scarlett Johansson')
    print(x)