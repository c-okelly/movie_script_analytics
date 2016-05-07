# Author Conor O'Kelly

"""
This is main file used in the preperation of data
"""

import pickle, os
import script_object
from script_object import MoveDataNotFound
import Data_phraser

def main():

    ### Call function to turn raw html files into text files
    file_directory = "Data/scripts_html/"
    save_directory = "Data/scripts_text/"
    # Data_phraser.run_text_cleaner_for_directory(file_directory,save_directory)

    ### Create array of all file names in saved directory

    # Find all files in directory and run them through clean_html_and_save_to_file
    list_all_files = os.listdir(save_directory)
    # Clean list
    cleaned_list = [file_name for file_name in list_all_files if file_name[0] != "."]

    print(len(cleaned_list), "Scripts to be converted")

    ### Create new directory to save into

    finished_objects = []
    failed_objects = []

    ### Go through files and build speech object and add to array to be pickled.
    ###  If error save error message and add to not not finished array


    start_range = 1000
    finished_range = 1100
    count = start_range

    print(start_range,finished_range)
    print(len(cleaned_list))
    for file in cleaned_list[start_range:finished_range]:

        file_name = file
        # If failure catch error. Add file to list and continue on
        try:
            file_path = save_directory + file_name

            with open(file_path) as file:
                current_text_file = file.read()
            current_script_object = script_object.Script(current_text_file,file_name)
            # Add object to array
            finished_objects.append(current_script_object)

            # Error messages
            print("count "+str(count)+". Chars words not mapped to char =>",current_script_object.info_dict.get("percent_unknown_words"))
            print("Total words",str(current_script_object.info_dict.get("total_words"))+". Speech,"+ str(current_script_object.info_dict.get("percent_speech"))+". Description " + str(current_script_object.info_dict.get("percent_description")))
            print("IMDB code is ", current_script_object.info_dict.get("imdb_code"))
            count += 1

        except MoveDataNotFound:
            print("\nThe IMDB could not be found for ", file_name)
            failed_objects.append([file_name,"IMDB dict failure"])
            count += 1

        except Exception as E:
            print("\nFile",file_name,"could not be converted into an ojbect. Error was ",E)
            failed_objects.append([file_name,E])
            count += 1

        if count % 30 == 0:
            pickle_file = "Data/Pickled_objects/object_list_"+str(count)+".dat"

            with open(pickle_file,"wb") as f:
                pickle.dump(finished_objects,f)

            finished_objects = []


    print(len(finished_objects))
    print(len(failed_objects))
    print(failed_objects)

    # Pickle list
    name = "Data/Pickled_objects/" + str(count) + ".dat"
    pickle_file = name

    with open(pickle_file,"wb") as f:
        pickle.dump(finished_objects,f)


    return failed_objects


    ### Allow user to rerun files that did no run one at a time
    ### Allowing to update IMDB search term if that was source of failure. If not rerun add to failed.

def run_individual_file(file_path,save_directory,file_name,search_name=0):
    pass

def failed_files(input_list):

    save_directory = "Data/scripts_text/"
    finished_objects = []
    failed_objects = []

    count = 1
    for file in input_list:

        # try:
        file_name = file[0]
        # search_name = file[1]
        # If failure catch error. Add file to list and continue on
        # try:
        file_path = save_directory + file_name

        with open(file_path) as file:
            current_text_file = file.read()
        current_script_object = script_object.Script(current_text_file,file_name)
        # Add object to array
        finished_objects.append(current_script_object)

        # Error messages
        print("count "+str(count)+". Chars words not mapped to char =>",current_script_object.info_dict.get("percent_unknown_words"))
        print("Total words",str(current_script_object.info_dict.get("total_words"))+". Speech,"+ str(current_script_object.info_dict.get("percent_speech"))+". Description " + str(current_script_object.info_dict.get("percent_description")))
        print("IMDB code is ", current_script_object.info_dict.get("imdb_code"))
        count += 1

        # except MoveDataNotFound:
        #     print("\nThe IMDB could not be found for ", file_name)
        #     failed_objects.append([file_name,"IMDB dict failure"])
        #     count += 1
        #
        # except Exception as E:
        #     print("\nFile",file_name,"could not be converted into an ojbect. Error was ",E)
        #     failed_objects.append([file_name,E])
        #     count += 1
        #
        #     if count % 30 == 0:
        #         pickle_file = "Data/failed_objects/object_list_"+str(count)+".dat"
        #
        #         with open(pickle_file,"wb") as f:
        #             pickle.dump(finished_objects,f)

                # finished_objects = []
    print(len(failed_objects))
    print(failed_objects)

    # Pickle list
    name = "Data/failed_objects/" + str(count) + ".dat"
    pickle_file = name

    with open(pickle_file,"wb") as f:
        pickle.dump(finished_objects,f)


if __name__ == '__main__':
    # main()

    failed_object_arrays = [['Crazylove.txt', 'Crazy-love'], ["Dave-Barry's-Complete-Guide-to-Guys.txt", 'Complete Guide to Guys'], ['Day-the-Clown-Cried,-The.txt', 'the day the clown cried'], ['Dry-White-Season,-A.txt', 'dry white season'], ['Ed-TV.txt', 'edtv'], ['Evil-Dead-II-Dead-by-Dawn.txt', 'Evil dead II'], ['Fright-Night-(1985).txt', 'Fright night'], ['Frozen-(Disney).txt', 'Frozen'], ['Adventures-of-Buckaroo-Banzai-Across-the-Eighth-Dimension,-The.txt', 'Adventures of buckaroo banzai'], ['Airplane-2-The-Sequel.txt', 'Airplane II'], ['Alien-3.txt', 'Alien 3'], ['American-Shaolin-King-of-Kickboxers-II.txt', 'IMDB dict failure'], ['Arctic-Blue.txt', 'arctic blue'], ["Avventura,-L'-(The-Adventure).txt", 'IMDB dict failure'], ['Batman-2.txt', 'batman II'], ['Blast-from-the-Past,-The.txt', 'IMDB dict failure'], ['Boondock-Saints-2-All-Saints-Day.txt', 'IMDB dict failure'], ['ghost_ship_info.txt', 'IMDB dict failure'], ['Ghostbusters-2.txt', 'IMDB dict failure'], ['Glengarry-Glen-Gross.txt', 'IMDB dict failure'], ['Grosse-Point-Blank.txt', 'IMDB dict failure'], ['Harold-and-Kumar-Go-to-White-Castle.txt', 'IMDB dict failure'], ['Hellboy-2-The-Golden-Army.txt', 'IMDB dict failure'], ['Hellraiser-3-Hell-on-Earth.txt', 'IMDB dict failure'], ['index.txt', 'IMDB dict failure'], ['Indiana-Jones-and-the-Raiders-of-the-Lost-Ark.txt', 'IMDB dict failure'], ['Indiana-Jones-IV.txt', 'IMDB dict failure'], ['Jennifer-Eight.txt', 'IMDB dict failure'], ['Jurassic-Park-The-Lost-World.txt', 'IMDB dict failure'], ['Kill-Bill-Volume-1-&-2.txt', 'IMDB dict failure'], ['Rambo-First-Blood-II-The-Mission.txt', 'IMDB dict failure'], ['Return-of-the-Apes.txt', 'IMDB dict failure'], ['Sandlot-Kids,-The.txt', 'IMDB dict failure'], ['Spare-Me.txt', 'IMDB dict failure'], ['Star-Wars-A-New-Hope.txt', 'IMDB dict failure'], ['Star-Wars-Attack-of-the-Clones.txt', 'IMDB dict failure'], ['Star-Wars-Return-of-the-Jedi.txt', 'IMDB dict failure'], ['Star-Wars-Revenge-of-the-Sith.txt', 'IMDB dict failure'], ['Star-Wars-The-Empire-Strikes-Back.txt', 'IMDB dict failure'], ['Star-Wars-The-Force-Awakens.txt', 'IMDB dict failure'], ['Star-Wars-The-Phantom-Menace.txt', 'IMDB dict failure'], ['Stuntman,-The.txt', 'IMDB dict failure'], ['Sugar.txt', AttributeError("'NoneType' object has no attribute 'getText'",)], ['Surfer-King,-The.txt', 'IMDB dict failure'], ['Terminator-2-Judgement-Day.txt', 'Terminator 2'], ['Three-Kings-(Spoils-of-War).txt', 'Three kings'], ['Three-Men-and-a-Baby.txt', 'IMDB dict failure'], ['Walk-to-Remember,-A.txt', 'IMDB dict failure'], ['White-Jazz.txt', 'IMDB dict failure'], ['Withnail-and-I.txt', 'IMDB dict failure']]
    failed_files(failed_object_arrays)