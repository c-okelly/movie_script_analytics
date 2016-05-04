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

        # Call array builder function
        self.__create_object_arrays_from_script()

        # Finish building objects
        self.__finish_building_objects()

        # Add data to script_info_dict if imdb data exists
        if self.imdb_dict != None:
            self.__extract_data_from_movie()

        # Testing
        # print(len(self.__speech_object_array),len(self.__description_object_array),len(self.__scene_object_array))
        # for i in self.__speech_object_array:
        #     print(i.speech_count)



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

    # Main algorithm to sort through through script and create the correct objects from text sections
    def __create_object_arrays_from_script(self):

        # print("Start")
        text_string = self.script
        total_words = len(re.findall("\w+",text_string)) # Create count of total words
        current_word_count = 0      # Create varialbe for currnet word count

        # Generate string list
        string_list = self.__return_text_list_in_sections(text_string)


        # Cycle through string list and sort. Call function to create object and add to correct array.
        for text_section in string_list:

            # Generate percentage count through script
            current_word_count += (len(re.findall("\w+",text_section)))
            percentage_count = current_word_count / total_words

            # Check first line to see if its all upper case => scene change => ext
            if text_section.split("\n")[0].isupper() and (re.search('\s{0,3}EXT\.', text_section)):
                self.__add_scene_change_ob_to_array(text_section,percentage_count,change_to_outside=1)


            # Check first line to see if its all upper case => scene change => int
            elif (text_section.split("\n")[0].isupper() and re.search('\s{0,3}INT\.', text_section)):
                self.__add_scene_change_ob_to_array(text_section,percentage_count,change_to_outside=0)


            # Check first line to see if its all upper case And that more then one line => character speech
            # Mark as discriptiong if more then 5 words without and / to seperate them
            elif text_section.split("\n")[0].isupper() and text_section.count("\n") > 1 and len(re.findall("\w+",text_section.split("\n")[0]))< 5:
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

    # Finishing building text objects using information collect after running over script once

    def __finish_building_objects(self):

        # Add speech count to each speech object
        no_speech_words = 0
        for i in self.__speech_object_array:
            no_speech_words += i.no_words

        current_speech_count = 0
        # print(no_speech_words,current_speech_count)

        for speech_ob in self.__speech_object_array:
            # Calculate percent through speech
            percent_through_speech = current_speech_count / no_speech_words
            # Set speech count
            speech_ob.add_speech_count(percent_through_speech)
            current_speech_count += speech_ob.no_words # Increase word count

        ### Scene objects   ###

        # Add finish point of scene using over all text count
        for no_i in range(len(self.__scene_object_array)):
            current_scene_ob = self.__scene_object_array[no_i]
            # Take next object in array and take start value. Set as end value for current scene object
            try:
                next_scene_ob = self.__scene_object_array[no_i+1]
                current_finish = next_scene_ob.start_count
                current_scene_ob.add_scene_finish_point(current_finish)
            except IndexError:
                # No more object this is the last. Ends at 1
                current_scene_ob.add_scene_finish_point(1)

        # Add object references to scene object array.
        for scene_ob in self.__scene_object_array:
            scene_start = scene_ob.start_count
            scene_finish = scene_ob.finish_count
            print(scene_start,scene_finish)
            # Get objects in the specified range and merge into list
            speech_objects = self.return_object_of_type_in_range(scene_start, scene_finish, speech_normal_count=1)
            description_objects = self.return_object_of_type_in_range(scene_start, scene_finish, discription=1)
            all_text_objects_in_scene = speech_objects + description_objects
            # Add object array to current scene object






    # Extract date from moive
    def __extract_data_from_movie(self):

        # Words counts
        total_words = len(re.findall("\w+",self.script))
        # Done with loop to be more accurate and remove all names
        no_speech_words = 0
        for i in self.__speech_object_array:
            no_speech_words += i.no_words

        no_discritption_words = len(re.findall("\w+",self.return_string_all_discription()))
        precent_of_speech = no_speech_words / total_words
        precent_of_discription = no_discritption_words / total_words

        # Words per a minute
        gen_words_per_min = total_words / self.imdb_dict.get("Runtime")
        speech_words_per_min = no_speech_words / self.imdb_dict.get("Runtime")
        disciription_words_per_min = no_discritption_words / self.imdb_dict.get("Runtime")
        # print(total_words,gen_words_per_min,speech_words_per_min,disciription_words_per_min)

        # Generate character list
        character_dict = self.__generate_dict_of_characters()

        # Character info
        no_characters = 0 # Must speak twice to avoid noise
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

        # Check the line is not either empty or all white space
        for line in split_on_empty_line:
            if (re.search("^\s*$",line)): # if line is only white space
                new_sections_list.append(temp_section_stirng)
                temp_section_stirng = ""
            elif len(line) > 0:
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

    # Fetch objects in specified range. It will return object pointers in a specified range.
    # Four main serach types. To search that array type set one of them equal to 1
    def return_object_of_type_in_range(self, start, finish, speech_normal_count=0, speech_speech_count=0, discription=0, scene=0): # Untested!!

        object_array = []

        selection_total = speech_normal_count + speech_speech_count + discription + scene
        # Check that only one option has been selected
        if selection_total > 1:
            print("More then one type was selected")
            object_array = None
        elif selection_total == 0:
            print("Type was not set")
            object_array = None

        # Search array
        elif speech_normal_count == 1: # Measured by general count
            search_array = self.__speech_object_array
            # Return correct objects
            for ob in search_array:
                if ob.count > start and ob.count < finish:
                    object_array.append(ob)

        elif speech_speech_count == 1: # Measured by speech count
            search_array = self.__speech_object_array
            # Return correct objects
            for ob in search_array:
                if ob.speech_count > start and ob.speech_count < finish:
                    object_array.append(ob)

        elif discription == 1:
            search_array = self.__description_object_array
            # Return correct objects
            for ob in search_array:
                if ob.count > start and ob.count < finish:
                    object_array.append(ob)

        # Scene object are returned depending on their start location
        elif scene:
            search_array = self.__scene_object_array
            # Return correct objects
            for ob in search_array:
                if ob.start_count > start and ob.start_count < finish:
                    object_array.append(ob)

        else:
            print("Type was not set")
            object_array = None

        return object_array

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

    def __generate_dict_of_characters(self):
        characters_dict = {}

        # For external info function => there are formatting requirements;
        # Dict passed should be a hold each character as a sub-dict where the character name is the key
        # Each sub-dict must contain the following keys and respective vars
        # 1. => "character_name":$char_name 2. => "no_appearances":$no_times_appeared

        # Generate Character name / no parts
        for speech_ob in self.__speech_object_array:
            character_name = speech_ob.character
            if character_name in characters_dict:
                characters_dict[character_name] = characters_dict[character_name] + 1
            else:
                characters_dict[character_name] = 1

        # Uses function in extre_character_info_for_movie_dict to map character to actor, add the meta critic rating, gender and find imdb character name
        updated_dict = (characters_dict) # Not calling to external just yet. Needs testing. Plus create a huge number of external html requests

        # print(characters_dict)
        # string = self.__get_string_character_speech("DOM")
        # print(string)

        return updated_dict

    def __get_chracter_info_by_name(self,seach_name):

        # Usd as builder for __add_extra_info_to_characters_dict

        sentiment = 0
        count = 0
        word_count = 0
        for object in self.__speech_object_array:
            if object.character == seach_name.upper():
                count += 1
                sentiment += object.sentimnet
                word_count += object.no_words

        average_sentiment = sentiment / count
        # Greate return dict
        info_dict = {"word_count": word_count, "sentiment": average_sentiment}

        return info_dict

    def __get_string_character_speech(self,search_name):

        return_string = ""
        for object in self.__speech_object_array:
            # print(object.text)
            if object.character == search_name.upper():
                return_string += object.cleaned_text
        # print(return_string)
        return return_string



    # This will attempt to capture the level of error that has occoured
    def generate_error_report(self):
        # Checks that at least 95 % of words make it into the object arrays.
        total_words = len(re.findall("\w+",self.script))
        no_speech_words = len(re.findall("\w+",self.return_string_of_all_speech()))
        no_discritption_words = len(re.findall("\w+",self.return_string_all_discription()))
        no_scene_words = len(re.findall("\w+",self.return_string_all_scene_changes()))
        words_captured = (no_speech_words+ no_discritption_words+ no_scene_words) / total_words

        # No Characters with less then 1 speaking part as percentage of whole => possible mis name if high

        # Amount of script capture by main characters


        return words_captured

if __name__ == '__main__':
    with open("../Data/scripts_text/17-Again.txt") as file:
        text_file = file.read()


    # try:
    test_script = Script(text_file,"17-Again.txt")

    # except Exception as e:
    #     print(e)
    #     print("Error")

    print(test_script)
    print(test_script.imdb_dict)
    print(test_script.generate_error_report())

