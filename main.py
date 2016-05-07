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


def failed_files(input_list):

    count = 1
    save_directory = "Data/scripts_text/"
    finished_objects = []
    failed_objects = []

    try:
        for file in input_list:

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

    except MoveDataNotFound:
        print("\nThe IMDB could not be found for ", file_name)
        failed_objects.append([file_name,"IMDB dict failure"])
        count += 1

    except Exception as E:
        print("\nFile",file_name,"could not be converted into an ojbect. Error was ",E)
        failed_objects.append([file_name,E])
        count += 1

        if count % 30 == 0:
            pickle_file = "Data/failed_objects/object_list_"+str(count)+".dat"

            with open(pickle_file,"wb") as f:
                pickle.dump(finished_objects,f)

            finished_objects = []


if __name__ == '__main__':
    # main()

    failed_object_arrays = [['Candle-to-Water.txt', 'Candle to water'], ['Chaos.txt', 'Chaos'], ['Christ-Complex.txt', 'IMDB dict failure'], ['Code-of-Silence.txt', 'IMDB dict failure'], ['Collateral-Damage.txt', 'IMDB dict failure'], ['Confidence.txt', 'IMDB dict failure'], ['Crazylove.txt', 'IMDB dict failure'], ['Crow-Salvation,-The.txt', 'IMDB dict failure'], ['Custody.txt', 'IMDB dict failure'], ["Dave-Barry's-Complete-Guide-to-Guys.txt", 'IMDB dict failure'], ['Day-the-Clown-Cried,-The.txt', 'IMDB dict failure'], ['Deception.txt', 'IMDB dict failure'], ['Dry-White-Season,-A.txt', 'IMDB dict failure'], ['Ed-TV.txt', 'IMDB dict failure'], ['Erik-the-Viking.txt', 'IMDB dict failure'], ['Evil-Dead-II-Dead-by-Dawn.txt', 'IMDB dict failure'], ['Extract.txt', 'IMDB dict failure'], ['Fatal-Instinct.txt', 'IMDB dict failure'], ['Four-Feathers.txt', 'IMDB dict failure'], ['Friday-the-13th-Part-VIII-Jason-Takes-Manhattan.txt', TypeError("unsupported operand type(s) for +: 'int' and 'str'",)], ['Fright-Night-(1985).txt', 'IMDB dict failure'], ['Frozen-(Disney).txt', 'IMDB dict failure'],
                            ['187.txt', 'IMDB dict failure'], ['30-Minutes-or-Less.txt', 'IMDB dict failure'], ['Above-the-Law.txt', 'IMDB dict failure'], ['Adventures-of-Buckaroo-Banzai-Across-the-Eighth-Dimension,-The.txt', 'IMDB dict failure'], ['After-School-Special.txt', 'IMDB dict failure'], ['Airplane-2-The-Sequel.txt', 'IMDB dict failure'], ['Alien-3.txt', 'IMDB dict failure'], ['American-Madness.txt', 'IMDB dict failure'], ['American-Shaolin-King-of-Kickboxers-II.txt', 'IMDB dict failure'], ['Amityville-Asylum,-The.txt', 'IMDB dict failure'], ["April-Fool's-Day.txt", 'IMDB dict failure'], ['Arcade.txt', 'IMDB dict failure'], ['Arctic-Blue.txt', 'IMDB dict failure'], ['Assignment,-The.txt', 'IMDB dict failure'], ['At-First-Sight.txt', 'IMDB dict failure'], ['Authors-Anonymous.txt', 'IMDB dict failure'], ["Avventura,-L'-(The-Adventure).txt", 'IMDB dict failure'], ['Bachelor-Party.txt', 'IMDB dict failure'], ['Bad-Country.txt', 'IMDB dict failure'], ['Bad-Dreams.txt', 'IMDB dict failure'], ['Batman-2.txt', 'IMDB dict failure'], ['Battle-of-Shaker-Heights,-The.txt', 'IMDB dict failure'], ['Benny-&-Joon.txt', 'IMDB dict failure'], ['Big-White,-The.txt', 'IMDB dict failure'], ['Blast-from-the-Past,-The.txt', 'IMDB dict failure'], ['Boondock-Saints,-The.txt', 'IMDB dict failure'], ['Boondock-Saints-2-All-Saints-Day.txt', 'IMDB dict failure'],
                            ['Game-6.txt', 'IMDB dict failure'], ['Gang-Related.txt', 'IMDB dict failure'], ['ghost_ship_info.txt', 'IMDB dict failure'], ['Ghostbusters-2.txt', 'IMDB dict failure'], ['Glengarry-Glen-Gross.txt', 'IMDB dict failure'], ['Godfather-Part-II.txt', "Failed to find OMDBAPI page for the movie / actor code nm0339589"], ['Gone-in-60-Seconds.txt', 'IMDB dict failure'], ['Grand-Theft-Parsons.txt', 'IMDB dict failure'], ['Grosse-Point-Blank.txt', 'IMDB dict failure'], ['Hackers.txt', 'IMDB dict failure'], ['Hall-Pass.txt', 'IMDB dict failure'], ['Happy-Birthday,-Wanda-June.txt', 'IMDB dict failure'], ['Hard-Rain.txt', 'IMDB dict failure'], ['Hard-to-Kill.txt', 'IMDB dict failure'], ['Harold-and-Kumar-Go-to-White-Castle.txt', 'IMDB dict failure'], ['Hebrew-Hammer,-The.txt', 'IMDB dict failure'], ['Hellboy-2-The-Golden-Army.txt', 'IMDB dict failure'], ['Hellraiser-3-Hell-on-Earth.txt', 'IMDB dict failure'], ["Henry's-Crime.txt", 'IMDB dict failure'], ['Highlander-Endgame.txt', 'IMDB dict failure'], ['Highlander.txt', 'IMDB dict failure'], ['How-to-Lose-Friends-&-Alienate-People.txt', 'IMDB dict failure'], ['index.txt', 'IMDB dict failure'], ['Indiana-Jones-and-the-Raiders-of-the-Lost-Ark.txt', 'IMDB dict failure'], ['Indiana-Jones-IV.txt', 'IMDB dict failure'], ['Inventing-the-Abbotts.txt', 'IMDB dict failure'], ['Jaws-2.txt', 'IMDB dict failure'], ['Jennifer-Eight.txt', 'IMDB dict failure'], ['Jurassic-Park-The-Lost-World.txt', 'IMDB dict failure'], ['Kill-Bill-Volume-1-&-2.txt', 'IMDB dict failure'], ['Labor-of-Love.txt', 'IMDB dict failure'], ['Lake-Placid.txt', 'IMDB dict failure'], ['Last-Flight,-The.txt', 'IMDB dict failure'], ['Legion.txt', 'IMDB dict failure'],
                            ['Rambo-First-Blood-II-The-Mission.txt', 'IMDB dict failure'], ['Replacements,-The.txt', 'IMDB dict failure'], ['Return-of-the-Apes.txt', 'IMDB dict failure'], ['Roughshod.txt', 'IMDB dict failure'], ['S.-Darko.txt', 'IMDB dict failure'], ['Sandlot-Kids,-The.txt', 'IMDB dict failure'], ['So-I-Married-an-Axe-Murderer.txt', 'IMDB dict failure'], ['Spare-Me.txt', 'IMDB dict failure'], ['Spartan.txt', 'IMDB dict failure'], ['Star-Wars-A-New-Hope.txt', 'IMDB dict failure'], ['Star-Wars-Attack-of-the-Clones.txt', 'IMDB dict failure'], ['Star-Wars-Return-of-the-Jedi.txt', 'IMDB dict failure'], ['Star-Wars-Revenge-of-the-Sith.txt', 'IMDB dict failure'], ['Star-Wars-The-Empire-Strikes-Back.txt', 'IMDB dict failure'], ['Star-Wars-The-Force-Awakens.txt', 'IMDB dict failure'], ['Star-Wars-The-Phantom-Menace.txt', 'IMDB dict failure'], ['Stuntman,-The.txt', 'IMDB dict failure'], ['style.css', 'IMDB dict failure'], ['Sugar-and-Spice.txt', 'IMDB dict failure'], ['Sugar.txt', AttributeError("'NoneType' object has no attribute 'getText'",)], ['Surfer-King,-The.txt', 'IMDB dict failure'], ['Surrogates.txt', 'IMDB dict failure'], ['Suspect-Zero.txt', 'IMDB dict failure'], ['Tall-in-the-Saddle.txt', 'IMDB dict failure'], ['Terminator-2-Judgement-Day.txt', 'IMDB dict failure'], ['Three-Kings-(Spoils-of-War).txt', 'IMDB dict failure'], ['Three-Men-and-a-Baby.txt', 'IMDB dict failure'], ['Thunderbirds.txt', 'IMDB dict failure'], ['Timber-Falls.txt', 'IMDB dict failure'],
                            ['Tin-Men.txt', 'IMDB dict failure'], ['Twilight-New-Moon.txt', 'IMDB dict failure'], ['Walk-to-Remember,-A.txt', 'IMDB dict failure'], ['While-She-Was-Out.txt', 'IMDB dict failure'], ['White-Christmas.txt', 'IMDB dict failure'], ['White-Jazz.txt', 'IMDB dict failure'], ['Whiteout.txt', 'IMDB dict failure'], ["Who's-Your-Daddy.txt", 'IMDB dict failure'], ['Wild-Things-Diamonds-in-the-Rough.txt', 'IMDB dict failure'], ['Wind-Chill.txt', 'IMDB dict failure'], ['Withnail-and-I.txt', 'IMDB dict failure'], ['X-Files-Fight-the-Future,-The.txt', 'IMDB dict failure']
                            ]
    failed_files(failed_object_arrays)