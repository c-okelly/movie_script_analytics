# Author Conor O'Kelly

"""
This file will contain the script object. It will take the input of a string object and the name of the script.
Each object will the run functions of the script to generate data from it.
This results can then be called by attributes to be put into a csv document
"""

from text_objects import Speech,Scene_change,Discription
from information_apis import imdb_data_call
import re
import operator

class MoveDataNotFound(Exception):

    def __init__(self,movie_name):
        self.move_name = movie_name
    def __repr__(self):
        return "Failed to find OMDBAPI date for the movie " + self.move_name

class Script:

    def __init__(self,script_string,movie_file_name):
        # Set attributed from inputs. One script sting and assoicated file name
        self.script = script_string
        # Reformat movie file name
        self.file_name = movie_file_name
        self.movie_title = self.__return_cleaned_name(movie_file_name)

        #Attempt to fetch omdbapi data using info api
        try:
            self.imdb_dict = imdb_data_call(self.movie_title)
        except:
            self.imdb_dict = None
            raise MoveDataNotFound(movie_file_name)

        # Created script info dict
        self.script_info_dict = {}

        # Create arrays to hold different script object
        self.__speech_object_array = []
        self.__description_object_array = []
        self.__scene_object_array = []

        # Called array builder functions
        self.__create_object_arrays_from_script()

        # Add data to script_info_dict if imdb date exists

        if self.imdb_dict != None:
            self.__extract_data_from_movie()




    def __repr__(self):
        return "Moive script object of => " + self.movie_title + " file name => " + self.file_name

    def __return_cleaned_name(self,dirty_file_name):

        # Clean file name
        cleand_name = dirty_file_name.replace("-", " ").replace(".txt", "")

        # If last word in file is 'the' move it to front
        test_name = cleand_name.split()[-1].lower()
        if (test_name == "the"):
            cleand_name = cleand_name.replace(", The","").replace(", the","")
            cleaned_file_name = "The " + cleand_name
        else:
            cleaned_file_name = cleand_name

        return cleaned_file_name

    # Create text object
    def __create_object_arrays_from_script(self):

        # print("Start")
        text_string = self.script
        total_words = len(re.findall("\w+",text_string)) # Create count of total words
        current_word_count = 0      # Create varialbe for currnet word count

        # Generate string list
        string_list = self.__return_text_list_in_sections(text_string)


        # Cycle through string list and sort. Call function to create object and add to correct array.
        for text_section in string_list:

            #Generate percentage count through script
            current_word_count += (len(re.findall("\w+",text_section)))
            percentage_count = current_word_count / total_words

            # Check first line to see if its all upper case => scene change => ext
            if text_section.split("\n")[0].isupper() and (re.search('\s{0,3}EXT\.', text_section)):
                self.__add_scene_change_ob_to_array(text_section,percentage_count,change_to_outside=1)


            # Check first line to see if its all upper case => scene change => int
            elif (text_section.split("\n")[0].isupper() and re.search('\s{0,3}INT\.', text_section)):
                self.__add_scene_change_ob_to_array(text_section,percentage_count,change_to_outside=0)


            # Check first line to see if its all upper case And that more then one line => character speech
            elif text_section.split("\n")[0].isupper() and text_section.count("\n") > 1:
                self.__add_speech_ob_to_array(text_section,percentage_count)
                # Catches sections of discriptions that are in all caps. Normally words displayed on screen. Could be argued as speech????


            # Check if character name follows by item in brackets => character speech
            elif re.search("\A(\s*[A-Z]+?){1,2}\s*(\(.*\))?\s*\Z",text_section.split("\n")[0]):
                self.__add_speech_ob_to_array(text_section,percentage_count)

            # # Description section / others
            else:
                # If section is more the 70% whitespace discard it
                if (text_section.count(" ") > (len(text_section) * 0.7)):
                    # print(text_section, "Discarded")
                    pass

                # Normal discription section
                else:
                    self.__add_discription_ob_to_array(text_section,percentage_count)


    def __add_scene_change_ob_to_array(self,text,count,change_to_outside):

        scene_object = Scene_change(text,count,change_to_outside)
        self.__scene_object_array.append(scene_object)
        # print(text,"added to scene_change \n")

    def __add_speech_ob_to_array(self,text,count):

        speech_object = Speech(text,count)
        self.__speech_object_array.append(speech_object)
        # print(text, speech_object.character,"added to speed\n")

    def __add_discription_ob_to_array(self,text,count):

        discription_object = Discription(text,count)
        self.__description_object_array.append(discription_object)
        # print(text,"added to discription\n")

    def __return_text_list_in_sections(self,text_file):

        # Split text on lines break
        split_on_empty_line = re.split("\n", text_file)
        split_on_empty_line.append("") # Add empty item to end of list

        # Cycle through item in list. If line has content add to new string.
        # If line empty append new string to list and reset new string.
        # Will break section up on empty line breaks. This can def be done better but I care not.

        new_sections_list = []
        temp_section_stirng = ""

        for line in split_on_empty_line:
            if len(line) > 0:
                temp_section_stirng += line + "\n"
            else:
                new_sections_list.append(temp_section_stirng)
                temp_section_stirng = ""

        # Remove items that have a length of 0
        no_empty_list_item = []
        for section in new_sections_list:
            if (len(section) != 0):
                no_empty_list_item.append(section)

        return no_empty_list_item

    # Extract date from moive
    def __extract_data_from_movie(self):

        # Words counts
        total_words = len(re.findall("\w+",self.script))
        no_speech_words = len(re.findall("\w+",self.return_string_of_all_speech()))
        no_discritption_words = len(re.findall("\w+",self.return_string_all_discription()))

        # Words per a minute
        gen_words_per_min = total_words / self.imdb_dict.get("Runtime")
        speech_words_per_min = no_speech_words / self.imdb_dict.get("Runtime")
        disciription_words_per_min = no_discritption_words / self.imdb_dict.get("Runtime")
        # print(total_words,gen_words_per_min,speech_words_per_min,disciription_words_per_min)

        # Generate character list
        character_dict = self.generate_dict_of_characters()

        # Character info
        no_characters = 0
        no_characters_speak_more_then_5_perent = 0
        no_characters_more_20_percent = 0
        average_character_sentiment = 0
        no_characters_overall_positive = 0
        no_characters_overall_negative = 0
        no_characters_overall_neutral = 0

        # Analysis of sentiment throughout the movie
        overall_sentiment = 0


        # Averages of speech words in different sections

        # Types of words used in the movie => vocab /

        # Catagories of language used => adverbs / adjectives


    def __return_object_of_type_in_range(self,start,finish,type): # Untested!!

        if type == "speech":
            search_array = self.__speech_object_array
        elif type == "discription":
            search_array = self.__description_object_array
        elif type == "scene":
            search_array = self.__scene_object_array



    def update_imdb_dict(self,new_search_name):
        try:
            self.imdb_dict = imdb_data_call(new_search_name)
            self.__extract_data_from_movie()
        except:
            raise MoveDataNotFound(new_search_name)

        return 1

    def return_string_of_all_speech(self):

        speech_string = ""
        for speech_ob in self.__speech_object_array:
            speech_string += speech_ob.text
        return speech_string

    def return_string_all_discription(self):

        discription_string = ""
        for discrip_ob in self.__description_object_array:
            discription_string += discrip_ob.text
        return discription_string

    def return_string_all_scene_changes(self):

        scene_string = ""
        for scene_ob in self.__scene_object_array:
            scene_string += scene_ob.text
        return scene_string

    def generate_dict_of_characters(self):
        characters_dict = {}

        for speech_ob in self.__speech_object_array:
            character_name = speech_ob.character
            if character_name in characters_dict:
                characters_dict[character_name] = characters_dict[character_name] + 1
            else:
                characters_dict[character_name] = 1

        updated_dict = self.__add_extra_info_to_characters_dict(characters_dict)

        return updated_dict

    def __add_extra_info_to_characters_dict(self,characters_dict):

        character_list = []
        # Create list of characters that are in the movie
        for character in characters_dict:
            character_list.append([character, characters_dict[character]])
        # Sorted list by number of appearances in movie
        sorted_character_list = sorted(character_list, key=lambda x:x[1],reverse=True)
        print(sorted_character_list)





    # Checks that at least 95 % of words make it into the object arrays.
    def test_words_all_there(self):
        total_words = len(re.findall("\w+",self.script))
        no_speech_words = len(re.findall("\w+",self.return_string_of_all_speech()))
        no_discritption_words = len(re.findall("\w+",self.return_string_all_discription()))
        no_scene_words = len(re.findall("\w+",self.return_string_all_scene_changes()))
        return total_words > (no_speech_words+ no_discritption_words+ no_scene_words) * 0.9

if __name__ == '__main__':
    with open("../Data/scripts_text/Avengers,-The.txt") as file:
        text_file = file.read()

    test_script = Script(text_file,"Avengers,-The.txt")

    print(test_script)
    print(test_script.imdb_dict)
    print(test_script.test_words_all_there())

    print(len([['REMEMBER', 1], ['THE HULK', 1], ['WHERE DID', 1], ['WEASELLY THUG', 1], ['OLD MAN', 1], ['SON OF', 1], ['AND KNOCKS', 1], ['GUESS', 1], ['WE GOT', 1], ['INTERCUTS', 1], ['WHAT ARE', 1], ['HOW DID', 1], ['FLYING', 1], ['DID', 1], ['YOU', 1], ['YOUNG SHIELD', 1], ['THOR CHARGES', 1], ['TARGET', 1], ['SHOOTS THROUGH', 1], ['MONTAGE', 1], ['CLOUD OF', 1], ['JULES', 1], ['WE', 1], ['THE COMPUTER', 1], ['ROGER', 1], ['THE GRENADE', 1], ['GALAGA PLAYER', 1], ['AM', 1], ['TELL', 1], ['PEGGY', 1], ['TONY STEVE', 1], ['SENATOR BOYNTON', 1], ['IT WOULD', 1], ['THOR LEAPS', 1], ['SHIELD AGENT', 1], ['SCRIPTS', 1], ['GOT', 1], ['AN IMPRESSIVE', 1], ['MISSED YOU', 1], ['FLY YOU', 1], ['RAISE THE', 1], ['STOP LYING', 1], ['SOON AS', 1], ['SMASHING INTO', 1], ['YOU LET', 1], ['STEVE TONY', 1], ['PEPPER POTTS', 1], ['CONTROL', 1], ['LIFT FANS', 1], ['SHIELD BASE', 1], ['BANNER SUDDENLY', 1], ['HOW MANY', 1], ['WE WERE', 1], ['PILOT', 1], ['GOLD', 1], ['MIGHTY', 1], ['KNOCKS HIM', 1], ['SHOCKWAVE THAT', 1], ['DIRECTOR', 1], ['LEVIATHAN IN', 1], ['THOR BACKHANDS', 1], ['TONY LOOKS', 1], ['YOU MAY', 1], ['HE ATTACKS', 1], ['NO HARD', 1], ['YOU BROUGHT', 1], ['THANK YOU', 1], ['THIS', 1], ['THE MASSIVE', 1], ['BUT', 1], ['BEFORE', 1], ['BANNER LOOKS', 1], ['CUT', 1], ['FURY FIRES', 1], ['HE MADE', 1], ['INSIDE THE', 1], ['ON', 1], ['WHAT DO', 1], ['WAITRESS', 1], ['BANNER IS', 1], ['TONY AND', 1], ['HULK', 1], ['SAVE THE', 1], ['ARE YOU', 1], ['THE END', 1], ['HE LOOKS', 1], ['AN', 1], ['IRON', 1], ['HE DIVES', 1], ['BREAKS OFF', 1], ['LOKI MEANS', 1], ['HOW DOES', 1], ['THIS IS', 1], ['NATASHA BANNER', 1], ['HE HAS', 1], ['ALWAYS', 1], ['IT GOES', 1], ['THEY NEED', 1], ['TAKES US', 1], ['YOU WANT', 1], ['ATTENDING WOMAN', 1], ['THE STARK', 1], ['NASA SCIENTIST', 1], ['SPIKING', 1]]))
