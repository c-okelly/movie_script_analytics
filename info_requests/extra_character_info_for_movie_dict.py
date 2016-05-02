# Author Conor O'Kelly

"""
This package will create have a main function that takes the argument of an imdb code.
This will then read in a csv file containing data for characters

"""

from bs4 import BeautifulSoup
import urllib.request as request
import urllib
import re

def scrape_and_format_page_info(imdb_code):

    # Create request url
    request_url = "http://www.imdb.com/title/" + imdb_code + "/"


    # Execute request and catch and errors
    # try:
    html_page = request.urlopen(request_url).read()

    cleaned_html = BeautifulSoup(html_page,"html.parser")
    cast_section = cleaned_html.find("table", {"class": "cast_list"}) # Find correct div and return all info including html

    only_rows = cast_section.findAll('tr') # Divide table up into rows

    character_dict = {}

    # Cycle through each row. Extra data and add dic to main character dict. Skip first row.
    for i in range(1,len(only_rows)):
        row = only_rows[i]

        # Find all individual cells in current row
        cells = row.findAll("td")

        # Skip cell 0 only image and get actor link and name
        actor_link_code = re.search("(nm\d+)",str(cells[1])).group().replace("/","")
        actor_name = cells[1].getText().strip().replace("\n","")
        # print(actor_link_code,actor_name)


        # Skip cell 2 only ... and find character information. Possibly multiple.
        character_link = re.findall("(ch\d+)",str(cells[3]))
        character_name = cells[3].getText().replace("\n","").split("/") # Remove html, strip, replace \n split \n


        # Create new character dict
        single_character = {"actor_name":actor_name,"actor_link_code":actor_link_code}

        # Add character name and links for each character
        count = 0
        for i in character_name:
            char_name = "character_name_" + str(count)
            single_character[char_name] = character_name[count].replace("(voice)","").strip() # Remove voice information
            char_link = "character_link_" + str(count)
            # Try as some character my not have links
            try:
                single_character[char_link] = character_link[count]
            except:
                single_character[char_link] = ""
            count += 1

        # print(single_character.get("actor_name"))

    return character_dict

def add_gender_and_meta_critic_info(character_dict):
    print("hi")

def combine_dicts_together(basic_dict,imdb_actor_info_dict):

    pass

if __name__ == '__main__':
    dict = scrape_and_format_page_info('tt0848228')
    new_dict = add_gender_and_meta_critic_info(dict)

