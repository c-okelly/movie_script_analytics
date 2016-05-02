# Author Conor O'Kelly

"""
This package will create have a main function that takes the argument of an imdb code.
This will then read in a csv file containing data for characters

"""

from bs4 import BeautifulSoup
import urllib.request as request
import urllib
import re
import regex

def scrape_and_format_page_info(imdb_code):

    # Create request url
    request_url = "http://www.imdb.com/title/" + imdb_code + "/" #fullcredits?ref_=tt_cl_sm#cast"


    # Execute request and catch and errors
    # try:
    html_page = request.urlopen(request_url).read()
    print("Page recieved")

    cleaned_html = BeautifulSoup(html_page,"html.parser")
    cast_section = cleaned_html.find("table", {"class": "cast_list"}) # Find correct div and return all info including html

    only_rows = cast_section.findAll('tr') # Divide table up into rows

    character_dict = {}
    list_of_characters = []

    # Cycle through each row. Extra data and add dic to main character dict. Skip first row.
    for i in range(1,len(only_rows)):
        row = only_rows[i]
        # Break loop when table row get down to uncredited cast members
        if len(row) == 1:
            break

        else:
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
                single_character[char_name] = character_name[count].replace("(voice)","").strip().upper() # Remove voice information
                char_link = "character_link_" + str(count)
                # Try as some character my not have links
                try:
                    single_character[char_link] = character_link[count]
                except:
                    single_character[char_link] = ""

                # Add character name to list of character names
                list_of_characters.append(i.replace("(voice)","").strip().upper())

                count += 1

            for i in range(len(character_name)):
                # Add character dict to multiple char dict.
                name = single_character.get("character_name_" + str(i))
                character_dict[name] = single_character # Whole name

            # print(single_character.get("actor_name"),single_character.get("character_name_0"))

    character_dict['list_of_characters'] = list_of_characters

    return character_dict

def add_gender_and_meta_critic_info(character_dict):
    pass
def combine_dicts_together(basic_dict,imdb_actor_info_dict):

    # for i in range(0,4):
    #     name = basic_dict[i][0]
    #     print(name)



    character_list = imdb_actor_info_dict.get("list_of_characters")
    character_string = ",".join(character_list)
    print(character_string)

    closest_match = regex.search(r",(CLINT){i},",character_string , regex.BESTMATCH).group()
    print(closest_match)

    pass

if __name__ == '__main__':
    character_list = [['TONY', 134], ['NICK FURY', 118], ['BANNER', 80], ['STEVE', 77], ['NATASHA', 74], ['LOKI', 74], ['THOR', 50], ['CONTEXT NAME', 50], ['AGENT PHIL', 46], ['CAPTAIN AMERICA', 43], ['PEPPER', 27], ['IRON MAN', 27], ['CLINT BARTON', 23], ['AGENT MARIA', 22], ['BLACK WIDOW', 20], ['WORLD SECURITY', 18], ['SELVIG', 15], ['JARVIS', 11], ['HAWKEYE', 11], ['SECURITY GUARD', 8], ['THE OTHER', 8], ['LUCHKOV', 6], ['OUTSIDE THE', 3], ['POLICE SERGEANT', 3], ['LITTLE GIRL', 3], ['BARTON', 3], ['SHIELD SCIENTIST', 2], ['ALPHA 11', 2], ['HELMSMAN', 2], ['ELDER GERMAN', 2], ['THE AVENGERS', 2], ['BACK AT', 2], ['YOUNG COP', 2], ['AGENT JASPER', 2], ['THE STARK', 1], ['SHIELD BASE', 1], ['ESCORT 606', 1], ['THE GRENADE', 1], ['HOW MANY', 1], ['INTERCUTS', 1], ['PILOT', 1], ['WAITRESS', 1], ['INSIDE THE', 1], ['STOP LYING', 1], ['TONY LOOKS', 1], ['SMASHING INTO', 1], ['PEGGY', 1], ['IRON', 1], ['TARGET', 1], ['ATTENDING WOMAN', 1], ['MIGHTY', 1], ['YOUNG SHIELD', 1], ['SHIELD AGENT', 1], ['GALAGA PLAYER', 1], ['HE MADE', 1], ['JULES', 1], ['THE END', 1], ['HE LOOKS', 1], ['UNKNOWN', 1], ['IT WOULD', 1], ['FURY FIRES', 1], ['NASA SCIENTIST', 1], ['MONTAGE', 1], ['FLYING', 1], ['WEASELLY THUG', 1], ['CONTROL', 1], ['THOR CHARGES', 1], ['GOLD', 1], ['SOON AS', 1], ['TONY STEVE', 1], ['STEVE TONY', 1], ['CUT', 1], ['FLY YOU', 1], ['NATASHA BANNER', 1], ['HOW DOES', 1], ['SENATOR BOYNTON', 1], ['HULK', 1], ['THIS IS', 1], ['BEFORE', 1], ['PEPPER POTTS', 1], ['OLD MAN', 1], ['SCRIPTS', 1], ['THE', 1]]

    dict = scrape_and_format_page_info('tt0848228')
    # new_dict = add_gender_and_meta_critic_info(dict)
    combine_dicts_together(character_list,dict)

