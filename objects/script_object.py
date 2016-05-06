# Author Conor O'Kelly

"""
This file will contain the script object. It will take the input of a string object and the name of the script.
Each object will the run functions of the script to generate data from it.
This results can then be called by attributes to be put into a csv document
"""

from text_objects import Speech,Scene_change,Discription,TextWorker
from information_apis import imdb_data_call
import re
import operator
import numpy as np
import nltk
import extra_character_info_for_movie_dict

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
        # Fine tunning for sorting need here and in the splitter function.
        for text_section in string_list:

            # Generate percentage count through script
            current_word_count += (len(re.findall("\w+",text_section)))
            percentage_count = current_word_count / total_words

            ### Scene Change
            # Check first line to see if its all upper case => scene change => ext
            if text_section.split("\n")[0].isupper() and (re.search('\s{0,3}EXT\.', text_section)):
                self.__add_scene_change_ob_to_array(text_section,percentage_count,change_to_outside=1)


            # Check first line to see if its all upper case => scene change => int
            elif (text_section.split("\n")[0].isupper() and re.search('\s{0,3}INT\.', text_section)):
                self.__add_scene_change_ob_to_array(text_section,percentage_count,change_to_outside=0)

            ### Speech
            # Check first line to see if its all upper case And that more then one line => character speech
            # Mark as discriptiong if more then 5 words without and / to seperate them

            # Third first line does not containtd the word omit / ommitted
            # Forth check => loods for time / date in format of -month/month(?), 1927- for the first line
            elif text_section.split("\n")[0].isupper() and text_section.count("\n") > 1 and len(re.findall("\w+",text_section.split("\n")[0]))< 5 and \
                    not re.search("(\s+OMIT\s*)|(\s+OMITTED\s*)",text_section.split("\n")[0]) \
                    and not re.match("^\s+-(\w+\s{0,3},?/?){0,4}(\s\d{0,5})?-",text_section.split("\n")[0]):
                # print(re.match("^\s+-(\w+\s{0,3},?/?){0,4}(\s\d{0,5})?-",text_section.split("\n")[0]))
                # print(text_section.split("\n")[0])
                self.__add_speech_ob_to_array(text_section,percentage_count)
                # Catches sections of discriptions that are in all caps. Normally words displayed on screen. Could be argued as speech????


            # Check if character name follows by item in brackets => character speech Check first line does not containtd the word omit
            ###     Only idenfifying orphaned speech sections at this moment    ###
            elif re.search("\A(\s*[A-Z]+?){1,2}\s*(\(.*\))?\s*\Z",text_section.split("\n")[0]) and not re.search("(\s+OMIT\s*)|(\s+OMITTED\s*)",text_section.split("\n")[0]):
                self.__add_speech_ob_to_array(text_section,percentage_count)
                # else:
                #     print(text_section, "One")

            ### Discription / Other
            # # Description section / others
            else:
                # If section is more the 70% whitespace discard it
                if (text_section.count(" ") > (len(text_section) * 0.7)):
                    # print(text_section, "Discarded")
                    pass

                # Normal description section
                else:
                    # print(text_section)
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
            # Get objects in the specified range
            speech_objects = self.return_object_of_type_in_range(scene_start, scene_finish, speech_normal_count=1)
            description_objects = self.return_object_of_type_in_range(scene_start, scene_finish, discription=1)
            # Add object array to current scene object
            scene_ob.add_object_array(speech_objects,description_objects)

        # For each scene object call data builder.
        for scene_ob in self.__scene_object_array:
            scene_ob.build_data_dict()

        # Testing


    # Extract date from moive
    def __extract_data_from_movie(self):

        ### Words counts
        total_words = len(re.findall("\w+",self.script))
        # Done with loop to be more accurate and remove all names
        no_speech_words = 0
        for i in self.__speech_object_array:
            no_speech_words += i.no_words
        no_descritption_words = len(re.findall("\w+",self.return_string_all_discription()))
        no_scene_change_words = len(re.findall("\w+",self.return_string_all_scene_changes()))

        # Get total words that have been captured by the sorting algo => character name / odd sections ommited
        total_cleaned_words =  no_speech_words + no_descritption_words + no_scene_change_words

        # print(total_words,total_cleaned_words)

        ### Percentages
        percent_of_speech = no_speech_words / total_cleaned_words
        percent_of_description = no_descritption_words / total_cleaned_words

        ### Words per a minute
        gen_words_per_min = total_words / self.imdb_dict.get("Runtime")
        speech_words_per_min = no_speech_words / self.imdb_dict.get("Runtime")
        description_words_per_min = no_descritption_words / self.imdb_dict.get("Runtime")
        # print(total_words,gen_words_per_min,speech_words_per_min,disciription_words_per_min)

        ### Current stop point
        ### Generate character list
        imdb_movie_code = self.imdb_dict.get("imdbID")
        character_dict = self.__generate_dict_of_characters(imdb_movie_code)
        no_cleaned_speech_words = character_dict.get("no_cleaned_speech_words")
        print(character_dict)

        # Character info
        no_characters = len(character_dict) # Must speak twice to avoid noise
        # Character gender
        no_female_characters = 0
        female_words_spoken = 0
        no_male_characters = 0
        male_words_spoken = 0
        no_unknown_genders = 0
        unknown_gender_words = 0

        # Count gender
        for character in character_dict:
            # Get gender. Skip if int returned instead of a dict. As one dict used to store general information
            try:
                gender = character_dict.get(character).get("gender")
                no_words = character_dict.get(character).get("no_words")
            except AttributeError:
                gender = "list_array"
                no_words = 0

            # print(gender)
            if gender == "M":
                no_male_characters += 1
                male_words_spoken += no_words
            elif gender == "F":
                no_female_characters += 1
                female_words_spoken += no_words
            elif gender is None:
                no_unknown_genders += 1
                unknown_gender_words += no_words

        print(no_characters, no_female_characters,no_male_characters,no_unknown_genders)
        ## Calculate percent of words spoken in each parts
        # Zero division error
        try:
            percent_male_chars = no_male_characters / no_characters
        except ZeroDivisionError:
            percent_male_chars = 0
        try:
            percent_female_chars = no_female_characters / no_characters
        except ZeroDivisionError:
            percent_female_chars = 0
        try:
            percent_unknown_chars = no_unknown_genders / no_characters
        except ZeroDivisionError:
            percent_unknown_chars = 0
        # Percentages
        try:
            percent_male_words = male_words_spoken / no_cleaned_speech_words
        except ZeroDivisionError:
            percent_male_words = 0
        try:
            percent_female_words = female_words_spoken / no_cleaned_speech_words
        except ZeroDivisionError:
            percent_female_words = 0
        try:
            percent_unknown_words = unknown_gender_words / no_cleaned_speech_words
        except ZeroDivisionError:
            percent_unknown_words = 0

        print(percent_male_chars,percent_female_chars,percent_unknown_chars,percent_male_words,percent_female_words,percent_unknown_words)


        # Speaking parts
        no_chars_speak_more_5_perent = 0
        no_chars_speak_more_10_perent = 0
        no_chars_speak_more_20_percent = 0

        for character_1 in character_dict:
            current_char_percentage = character_dict.get(character_1).get("")
            if current_char_percentage >= 0.05:
                no_chars_speak_more_5_perent += 1
            if current_char_percentage >= 0.1:
                no_chars_speak_more_10_perent += 1
            if current_char_percentage >= 0.2:
                no_chars_speak_more_20_percent += 1


        ### Sentiment
        average_speech_sentiment = 0
        average_description_sentiment = 0
        overall_sentiment = 0

        # Character sentiment
        no_characters_overall_positive = 0
        no_characters_overall_negative = 0
        no_characters_overall_neutral = 0

        # Analysis of sentiment throughout the movie
        sentiment_plot_of_speech = 0
        sentiment_plot_of_description = 0
        overall_sentiment_plot = 0

        # Top 5 character dicts
        

        # Dict summaries for Scene

        # Averages of speech words in different sections

        # Categories of language used => adverbs / adjectives

        # No of unique non stop words => vocab measure

        # Actors scores
        score_top_5_actors = 0


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


        ### Algo to recombine all the line together
        ## => potentially usefull regex to search for sections that is marked after page break informally and continue => ^\s*(\w)?(\d{1,4}){1,5}\sCONTINUED:\s(\(\d{0,4}\))?(\s\d{1,4})?
        #
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

    def __generate_dict_of_characters(self,imdb_movie_code):
        characters_dict = {}

        # For external info function => there are formatting requirements;
        # Dict passed should be a hold each character as a sub-dict where the character name is the key
        ### Each sub-dict must contain the following keys and respective vars ###
        # 1. => "character_name":$char_name 2. => "no_appearances":$no_times_appeared

        # Generate Character name / no parts and store sub dicts in master dict
        for speech_ob in self.__speech_object_array:
            character_name = speech_ob.character
            if characters_dict.get(character_name):
                currenct_dict = characters_dict.get(character_name)
                currenct_dict["no_appearances"] += 1
            else:
                characters_dict[character_name] = {"character_name":character_name,"no_appearances":1}

        # print(characters_dict)

        ### Add no words for each character
        for character in characters_dict:
            current_char_name = characters_dict.get(character).get("character_name")
            character_string = self.__get_string_character_speech(current_char_name)
            # print(character_string)
            # Get no words and calculate percentage
            no_words_for_char = len(re.findall("\w+",character_string))
            # Insert
            characters_dict.get(character)["no_words"] = no_words_for_char


        ### Remove characters that do not have at least 50 words or their names are numbers
        # Generate new total of speech parts with noise characters removed
        # Create new characters dict
        cleaned_characters_dict = {}
        total_speech_cleaned = 0

        for character_1 in characters_dict:
            currenct_dict_1 = characters_dict.get(character_1)
            current_name_1 = currenct_dict_1.get("character_name")
            # Check that no words greater then 30 and name is not a number / number starting with letter and that at least 2 apperances
            if currenct_dict_1.get("no_words") > 30 and not re.match("^\w?\d{1,4}\w?$",current_name_1) and currenct_dict_1.get("no_appearances") >= 2:
                cleaned_characters_dict[current_name_1] = currenct_dict_1
                total_speech_cleaned += currenct_dict_1.get("no_words")
            else:
                pass

            # elif currenct_dict_1.get("no_words") < 30:
            #     print(currenct_dict_1, "not enough words \n")
            # elif re.match("^\w?\d{1,4}$",current_name_1):
            #     print(currenct_dict_1, "name is a number \n")
            # else:
            #     print(currenct_dict_1, "no matches \n")

        ### Add percentage of words from excluding noise eliminated
        for character_2 in characters_dict:
            current_dict_2 = characters_dict.get(character_2)
            no_words_for_char_2 = current_dict_2.get("no_words")
            try:
                percentage_of_speech = no_words_for_char_2 / total_speech_cleaned
            except ZeroDivisionError:
                percentage_of_speech = 0
            # Insert info into dict
            current_dict_2["percent_clean_speech"] = percentage_of_speech

        ### Sentiment plot for each character and average sentiment => plot will be done by generate average within a range

        for character_3 in cleaned_characters_dict:
            current_dict_3 = cleaned_characters_dict.get(character_3)
            char_name_3 = current_dict_3.get("character_name")

            # Get sections of object array for character
            ###  Variable to set ranges to select   ### ##special_key_value##
            range_selection = 0.05

            sent = self.__get_sentiment_plot_and_overall_sentiment(current_dict_3,char_name_3,range_selection)


                    ###     This Section should use language dict analysis    ###
        ### Text analysis of each character, no of unique non stop words => vocb, average sentence length

        # Create analysis function
        analysis_object = TextWorker()

        for character_4 in cleaned_characters_dict:
            current_dict_4 = cleaned_characters_dict.get(character_4)
            character_name_4 = current_dict_4.get("character_name")
            # Get character string
            character_string_4 = self.__get_string_character_speech(character_name_4)
            # Get language analysis dict
            language_analysis_dict = analysis_object.return_language_analysis_dict(character_string_4)

            # Carry out frequency dist calculation
            frequency_of_non_stop_words = self.__word_count_analysis(character_string_4)

            # print(character_name_4,frequency_of_non_stop_words)
            # Insert information into dict
            current_dict_4["language_analysis_dict"] = language_analysis_dict
            current_dict_4["freq_of_non_stop_words"] = frequency_of_non_stop_words


        #print("\n",cleaned_characters_dict)


        ### Uses function in extre_character_info_for_movie_dict to map character to actor,
        # add the meta critic rating, gender and find imdb character name
        updated_dict = extra_character_info_for_movie_dict.add_extra_info_to_current_dict(cleaned_characters_dict,imdb_movie_code)
        # Not calling to external just yet as creates a huge number of external html requests


        ### Add general script info found => no_cleaned_speech_words

        updated_dict["no_cleaned_speech_words"] = total_speech_cleaned

        return updated_dict

    ## Not used
    def __get_chracter_info_by_name(self,seach_name):

        # Usd as builder for __add_extra_info_to_characters_dict

        sentiment = 0
        count = 0
        word_count = 0
        for object in self.__speech_object_array:
            if object.character == seach_name.upper():
                count += 1
                sentiment += object.sentiment
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

    def __get_character_object_by_name_and_range(self,name,start_range,finish_range):

        obj_return_array = []

        range_objects = self.return_object_of_type_in_range(start=start_range,finish=finish_range,speech_normal_count=1)

        for obj in range_objects:
            if obj.character == name:
                obj_return_array.append(obj)

        return obj_return_array

    def __return_sentiment_summary_of_array(self,sentiment_array):

        no_non_zero_values = 0
        running_total_sentiment = 0

        # print(sentiment_array)

        if len(sentiment_array) > 0:
            for text_ob in sentiment_array:
                current_sentiment = text_ob.sentiment
                if abs(current_sentiment) > 0:
                    no_non_zero_values += 1
                    running_total_sentiment += current_sentiment
        else:
            average_sentiment = 0

        try:
            average_sentiment = running_total_sentiment / no_non_zero_values
        except ZeroDivisionError:
            average_sentiment = 0

        return average_sentiment

    ## To be used for refatoring of character analysis
    def __get_sentiment_plot_and_overall_sentiment(self,current_dict_3,char_name_3,range_selection):
        text_object_in_selected_ranges = []

        for i in np.arange(0,1,range_selection):
            start = i
            finish = i + range_selection
            current_range_3 = self.__get_character_object_by_name_and_range(char_name_3,start,finish)
            text_object_in_selected_ranges.append(current_range_3)

        # print(text_object_in_selected_ranges, len(text_object_in_selected_ranges))
        # Use range array to convert into plot
        sentiment_plot_array = []
        for sentiment_array in text_object_in_selected_ranges:
            avg_sent_for_section = self.__return_sentiment_summary_of_array(sentiment_array)
            sentiment_plot_array.append(avg_sent_for_section)


        # Calculate over all sentiment for character
        non_zero_items = 0
        for i in sentiment_plot_array:
            if abs(i) > 0:
                non_zero_items += 1

        try:
            over_all_sentiment = sum(sentiment_plot_array) / non_zero_items
        except ZeroDivisionError:
            over_all_sentiment = 0
        # print(char_name_3,over_all_sentiment)

        # # Insert sentiment information into dict
        current_dict_3["sentiment_plot"] = sentiment_plot_array
        current_dict_3["sentiment_plot_range"] = range_selection
        current_dict_3["overall_sentiment"] = over_all_sentiment

    def __word_count_analysis(self,string_to_be_analysed,length_frequency_array=10):

        default_stopwords = set(nltk.corpus.stopwords.words('english'))

        # Tokenize all words
        token_words = nltk.word_tokenize(string_to_be_analysed)

        # Remove words shorted then 1
        token_words = [word for word in token_words if len(word) > 2]
        # Remove numbers
        token_words = [word for word in token_words if not word.isnumeric()]
        # Lower case all words
        token_words = [word.lower() for word in token_words]
        # Remove stop words
        non_stop_words = [word for word in token_words if word not in default_stopwords]

        word_f_dist = nltk.FreqDist(non_stop_words)


        # Get top 10 words => default 10
        most_frequent_words = []
        for word, frequency in word_f_dist.most_common(length_frequency_array):
            most_frequent_words.append([word,frequency])
        # print(most_frequent_words)

        return most_frequent_words

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
    with open("../Data/scripts_text/12-Years-a-Slave.txt") as file:
        text_file = file.read()


    # try:
    test_script = Script(text_file,"12-Years-a-Slave.txt")

    print("Done!")

    # except Exception as e:
    #     print(e)
    #     print("Error")

    # print(test_script)
    # print(test_script.imdb_dict)
    # print(test_script.generate_error_report())

