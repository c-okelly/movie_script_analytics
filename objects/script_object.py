# Author Conor O'Kelly

"""
This file will contain the script object. It will take the input of a string object and the name of the script.
Each object will the run functions of the script to generate data from it.
This results can then be called by attributes to be put into a csv document
"""

from text_objects import Speech,Scene_change,Discription
from information_apis import imdb_data_call
import re

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

        # Attempt to fetch omdbapi data using info api
        # try:
        #     self.imdb_dict = imdb_data_call(self.movie_title)
        # except:
        #     raise MoveDataNotFound(movie_file_name)

        # Created script info dict
        self.script_info_dict = {}

        # Create arrays to hold different script object
        self.__speech_object_array = []
        self.__description_object_array = []
        self.__scene_object_array = []

        # Called array builder functions
        self.__create_object_arrays_from_script()

        # Add data to script_info_dict
        self.__extract_data_from_movie()


    def __repr__(self):
        return "Moive script object of => " + self.movie_title + "file name => " + self.file_name


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


    # Text text and sort
    def __create_object_arrays_from_script(self):

        print("Start")
        worked_text_file = self.script
        # print(worked_text_file)

        # Split text on lines break
        split_on_empty_line = re.split("\n", worked_text_file)
        split_on_empty_line.append("") # Add empty item to end of list

        # Cycle through item in list. If line has content add to new string.
        # If line empty append new string to list and reset new string.
        # Will break section up on empty line breaks

        new_string = ""
        new_contents_list = []
        for line in split_on_empty_line:
            if len(line) > 0:
                new_string += line + "\n"
            else:
                new_contents_list.append(new_string)
                new_string = ""

        for item in new_contents_list:
            print(item)
            print("break", len(item))


        test = split_on_empty_line[5:20]
        # for i in test:
        #     print(i)




        return 1

    def __extract_data_from_movie(self):

        return 1

    def update_imdb_dict(self,new_search_name):
        try:
            self.imdb_dict = imdb_data_call(new_search_name)
        except:
            raise MoveDataNotFound(new_search_name)

        return 1


if __name__ == '__main__':
    with open("../Data/scripts_text/Abyss,-The.txt") as file:
        text_file = file.read()

    test_script = Script(text_file,"Abyss,-The.txt")

    # print(test_script)