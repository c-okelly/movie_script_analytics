# Author Conor O'Kelly

"""
This file will contain the script object. It will take the input of a string object and the name of the script.
Each object will the run functions of the script to generate data from it.
This results can then be called by attributes to be put into a csv document
"""

from text_objects import Speech,Scene_change,Discription
from information_apis import imdb_data_call

class Script:

    def __init__(self,script,movie_title,script_imdb_id,infomation_dict):
        self.script = script
        self.movie_title = movie_title
        self.movei_imdb_id = script_imdb_id
        self.information_dict = infomation_dict
        self.script_dict = self.create_script_info_dict()

    # Match each of the sections depending on
    def create_script_info_dict(self):


        return 1

def create_script_object_from_name_and_file(script_text_file,file_name):

    # Clean file name
    cleand_name = file_name.replace("-", " ").replace(".txt", "")

    # If last word in file is the move it to front
    test_name = cleand_name.split()[-1].lower()
    if (test_name == "the"):
        cleand_name = cleand_name.replace(", The","").replace(", the","")
        cleand_name = "The " + cleand_name

    # Use imdb call to serach for meta date based on movie name
    meta_data = imdb_data_call(cleand_name)


    print(meta_data)

if __name__ == '__main__':
    with open("../Data/scripts_text/Abyss,-The.txt") as file:
        text_file = file.read()

    create_script_object_from_name_and_file(text_file,"Abyss,-The.txt")