# Author Conor O'Kelly

"""
This package will create have a main function that takes the argument of an imdb code.
Takes the associated cast page and create a dictionary of character name and actor name.
Will also have a function to retrieve the gender of the actors and their releated actor code
"""

from bs4 import BeautifulSoup
import urllib.request as request
import urllib
import re

def scrape_and_format_page_info(imdb_code):

    # Create request url
    request_url = "http://www.metacritic.com/person/" + imdb_code
    # print(request_url)


if __name__ == '__main__':
    pass

