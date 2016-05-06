# Author Conor O'Kelly

"""
This package will create have a main function that takes the argument of an imdb code and a character dict
It will match the character in the movie to an actor using imdb. Then add gender and meta critic rating of actor

This will then read in a csv file containing data for characters

There are two main varialbes on this page that may affect data output.
    First is the row count no to break on set in scrape_and_format_page_info. This limits the no of cast members in the dict generated
        Currently set to 25 or first section of credited members

    Second is the error margin on the regex fuzzy search. This currently allows for up to 15 insertions and 2 substitutions but tries without subs first

"""

from bs4 import BeautifulSoup
import urllib.request as request
import urllib
import re
import regex
import meta_critic_web_scraper

class UrlRequestFailed(Exception):
    def __init__(self,imdb_code):
        self.imdb_code = imdb_code
    def __repr__(self):
        return "Failed to find OMDBAPI page for the movie / actor code " + self.imdb_code


def scrape_and_format_page_info(imdb_code):

    # Create request url
    request_url = "http://www.imdb.com/title/" + imdb_code + "/fullcredits"


    # Execute request and catch and errors
    try:
        html_page = request.urlopen(request_url).read()
    except:
        raise UrlRequestFailed(imdb_code)

    # print("Page recieved")

    cleaned_html = BeautifulSoup(html_page,"html.parser")
    cast_section = cleaned_html.find("table", {"class": "cast_list"}) # Find correct div and return all info including html

    only_rows = cast_section.findAll('tr') # Divide table up into rows

    character_dict = {}
    list_of_characters = []

    row_count = 0
    # Cycle through each row. Extra data and add dic to main character dict. Skip first row.
    for i in range(1,len(only_rows)):
        row = only_rows[i]
        row_count += 1
        # Break loop when table row get down to uncredited cast members or after first 25 cast members
        if len(row) == 1:# or row_count > 25:
            pass

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
            single_character = {"actor_name":actor_name.strip(),"actor_link_code":actor_link_code}

            # Add character name and links for each character
            count = 0
            for i in character_name:
                char_name = "character_name_" + str(count).strip()
                name_to_inset = character_name[count].strip().upper()
                # print(name_to_inset)
                name_to_inset = re.sub("\((\s*\w+)*\)","",name_to_inset)# Remove information in brackets
                # print(name_to_inset)
                single_character[char_name] = name_to_inset # Remove voice information
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
                name = single_character.get("character_name_" + str(i)).strip()
                character_dict[name] = single_character # Whole name

            # print(single_character.get("actor_name"),single_character.get("character_name_0"))

    character_dict['list_of_characters'] = list_of_characters
    # print(character_dict)
    return character_dict

def add_gender_and_meta_critic_info(character_dict): # Add extra info to the dicts. Using sqllite db to minimise number of calls

    # To be reformatted in the future to use a database that is built with each new call.
    # Cut short as ran out of time for this part of the project. Will revisit later.

    # Cycle through each actor in dict
    for character in character_dict:
        current_dict = character_dict.get(character)

        current_actor_link_code = current_dict.get("actor_link_code")
        current_actor_name = current_dict.get("actor_name")

        # Add info to current dict using calls
        if current_actor_link_code != None:
            gender = get_gender_from_actor_id(current_actor_link_code)
        else:
            gender = None

        if current_actor_name != None:
            # print(current_actor_name)
            meta_critic_score = meta_critic_web_scraper.retieve_person_score(current_actor_name)
        else:
            meta_critic_score = None

        current_dict["gender"] = gender
        current_dict["meta_critic_score"] = meta_critic_score


    return character_dict

def get_gender_from_actor_id(actor_id):

    # Create request url
    request_url = "http://www.imdb.com/name/" + actor_id + "/"

    # Execute request and catch and errors
    try:
        html_page = request.urlopen(request_url).read()
    except:
        raise UrlRequestFailed(actor_id)

    cleaned_html = BeautifulSoup(html_page,"html.parser")
    actor_info_bar = cleaned_html.find("div", {"class": "infobar"}) # Find correct div and return all info including html

    cleaned_text = actor_info_bar.getText().lower()

    if "actor" in cleaned_text:
        gender = "M"
    elif "actress" in cleaned_text:
        gender = "F"
    else:
        gender = None

    return gender

def combine_dicts_together(basic_dict,imdb_actor_info_dict):

    # Take the list of character and turn into single string with ! before and after every character.
    # Had used , but might cause errors later
    character_list = imdb_actor_info_dict.get("list_of_characters")
    cleaned_character_list = []
    for char in character_list:
        cleaned_char = re.sub("\((\s*\w+.)*\){1,5}","",char).strip() # Remove information in brackets
        cleaned_character_list.append(cleaned_char)

    character_string = "!" + "!".join(cleaned_character_list) + "!"
    # print(cleaned_character_list)
    finished_combined_dict = {}

    for char_dict in basic_dict:

        # Set name equal to current character name. Use long character string to perform fuzzy regex search.
        script_character_name = basic_dict.get(char_dict).get("character_name")
        if not re.search("^\w?\d{1,4}",script_character_name.strip()): # Ensure character name is not only numbers => normally an error on sortings
            search_object = regex.search(r"!("+script_character_name+"){i<=15}!",character_string , regex.BESTMATCH) # Only insertions
            # print(script_character_name)
            #### Commented out as was adding noise only ####
            # if search_object == None: # If nothing found allows substitutions
            #     search_object = regex.search(r"!("+script_character_name+"){i<=10,s<=2}!",character_string , regex.BESTMATCH)

            if search_object == None and len(script_character_name.split(" ")) >= 2: # Seach using first half word and then second half
                script_character_name = script_character_name.split(" ")[0]
                search_object = regex.search(r"!("+script_character_name+"){i<=1}!",character_string, regex.BESTMATCH)

                # print(search_object, script_character_name)
            if search_object == None: # Allow search for substring with deletions
                search_object = regex.search(r"!("+script_character_name+"){d<=2}!",character_string , regex.BESTMATCH)
                # print(search_object, script_character_name, "3")


        else:
            search_object = None

        # print(script_character_name,search_object)

        # Try set result string as best match. If failed set as none
        try:
            closest_character_match = search_object.group()
            # Check that no two character names combined
            if closest_character_match.count("!")<= 2:
                closest_character_match = closest_character_match.replace("!","")
            else:
                print("Doulbe match. Error from extra_character_info_file combine function",closest_character_match,script_character_name)
                closest_character_match = None
        except:
            closest_character_match = None


        # print(script_character_name," matched to ",closest_character_match)
        # print(search_object, "\n")

        basic_dict_copy = basic_dict.get(char_dict)
        correct_imdb_dict = imdb_actor_info_dict.get(closest_character_match)
        # print(imdb_actor_info_dict)

        ###         Add to this section to change what information is combined into the final dict
        ###

        if correct_imdb_dict != None:
            # Merge imdb into basic
            actor_name = correct_imdb_dict.get("actor_name")
            actor_link_code = correct_imdb_dict.get("actor_link_code")
            # Insert into into
            basic_dict_copy["actor_name"] = actor_name
            basic_dict_copy["actor_link_code"] = actor_link_code

            # No of characters
            no_chars_in_dict = (len(correct_imdb_dict)-2)/2

            # Find match between closes_character_match and character name. Create variable of character link no
            for i in range(0,int(no_chars_in_dict)):
                if closest_character_match == correct_imdb_dict.get("character_name_" + str(i)):
                    full_character_name = correct_imdb_dict.get("character_name_" + str(i))
                    basic_dict_copy["full_character_name"] = full_character_name
                    character_link_no = correct_imdb_dict.get("character_link_" + str(i))
                    basic_dict_copy["character_link_no"] = character_link_no

        else:
            basic_dict_copy["actor_name"] = None
            basic_dict_copy["actor_link_code"] = None
            basic_dict_copy["character_link_no"] = None
            basic_dict_copy["full_character_name"] = None

        # Add results to return dict
        finished_combined_dict[basic_dict_copy.get("character_name")] = basic_dict_copy


    return finished_combined_dict

def add_extra_info_to_current_dict(basic_character_dict,imdb_movie_code):

    # Generate scrape dict from moive code
    imdb_scrape_dict = scrape_and_format_page_info(imdb_movie_code)

    partical_extened_dict = combine_dicts_together(basic_character_dict,imdb_scrape_dict)

    ## Add extra info => currently commented out
    completed_extened_dict = add_gender_and_meta_critic_info(partical_extened_dict)

    return completed_extened_dict

if __name__ == '__main__':
    character_list = [['TONY', 134], ['NICK FURY', 118], ['BANNER', 80], ['STEVE', 77], ['NATASHA', 74], ['LOKI', 74], ['THOR', 50], ['CONTEXT NAME', 50], ['AGENT PHIL', 46], ['CAPTAIN AMERICA', 43], ['PEPPER', 27], ['IRON MAN', 27], ['CLINT BARTON', 23], ['AGENT MARIA', 22], ['BLACK WIDOW', 20], ['WORLD SECURITY', 18], ['SELVIG', 15], ['JARVIS', 11], ['HAWKEYE', 11], ['SECURITY GUARD', 8], ['THE OTHER', 8], ['LUCHKOV', 6], ['OUTSIDE THE', 3], ['POLICE SERGEANT', 3], ['LITTLE GIRL', 3], ['BARTON', 3]]
    basic_character_dict = {}
    sub_char_dict = {}

    for i in character_list:
        sub_char_dict["character_name"] = i[0]
        sub_char_dict["no_appearances"] = i[1]
        basic_character_dict[i[0]] = sub_char_dict
        sub_char_dict = {}



    try:
        finished_dict = add_extra_info_to_current_dict(basic_character_dict,'tt0848228')
        print(finished_dict)

    except Exception as e:
        print(e)

