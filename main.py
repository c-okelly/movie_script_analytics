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



    ### Allow user to rerun files that did no run one at a time
    ### Allowing to update IMDB search term if that was source of failure. If not rerun add to failed.




if __name__ == '__main__':
    main()