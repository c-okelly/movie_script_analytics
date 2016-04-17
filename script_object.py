# Author Conor O'Kelly

"""
This file will contain the script object. It will take the input of a string object and the name of the script.
Each object will the run functions of the script to generate data from it.
This results can then be called by attributes to be put into a csv document
"""

class Script:

    def __init__(self,script,movie_title,script_imdb_id,infomation_dict):
        self.script = script
        self.movie_title = movie_title
        self.movei_imdb_id = script_imdb_id
        self.information_dict = infomation_dict
        self.script_dict = self.create_script_info_dict()

    def create_script_info_dict(self,):

        return 1