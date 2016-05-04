# Author Conor O'Kelly

# from vaderSentiment.vaderSentiment import sentiment as VS
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from collections import defaultdict

# Generalised analytsis functions # Abstract function
class TextBasedSection:

    def check_inheritance(self):
        print("hi")

    # Take text and return sentiment
    def sentiment_analytis_text(self,text_insert):

        text = text_insert

        token_text = tokenize.sent_tokenize(text)
        sid = SentimentIntensityAnalyzer()

        over_all_sentiment = 0
        count = 0

        for sentence in token_text:
            score = sid.polarity_scores(sentence)
            # Create over all sentiment score
            over_all_sentiment += score.get("compound")

            # If sentence is not neuteral add to sentence count for average
            if (score.get("compound") >  0.1):
                count += 1

        # Calculate average sentiment
        if count > 0:
            average_sentiment = over_all_sentiment/count
        else:
            average_sentiment = over_all_sentiment

        return average_sentiment

class Speech(TextBasedSection):

    def __init__(self,text,count):

        ## Should add average length of line

        self.text = text
        self.count = count
        # Percent point in speech - added later once whole script has been processed
        self.speech_count = 0
        # Error message if character names can't be found
        self.errors_in_processing = 0
        self.error_message = ""
        # Set together
        self.character = self.__return_character_name()
        self.multiple_characters = self.__check_multiple_characters()
        # Cleaned text version without character name
        self.cleaned_text = self.__cleaned_text()
        # Sentiment analysis averaged for section and returned.
        self.sentiment = self.sentiment_analytis_text(self.cleaned_text)
        self.no_words = self.__return_no_words()
        # Extra analysis on text => built incrementally using previous attributes
        # Average sentence legth
        self.avg_setenece_length = self.__avg_sentence_legth()

    def __repr__(self):
        return "Speech object for character " + self.character + ". Abs count = " + str(self.count) + "%. Speech count = " + str(self.speech_count) + "%"

    def __return_character_name(self):

        text = self.text

        # Regex to pull out character name
        try:
            # Test if only bracket word on first line and save as contextual speech section
            context_name = re.search("^\s*\(\w+(\s\w+){0,1}\)\s*$" ,text.split("\n")[0]).group()
            character_name = "Context name"
            self.errors_in_processing = 0
        except:
            # If name is not context name
            try:
                character_name = re.search("\s\w{2,}(\s\w{2,}){0,1}(/\w{2,}){0,}\s",text).group().strip()
                self.errors_in_processing = 0
            except:
                character_name = "Unknown"
                errors_in_processing = 1
                error_message = ("Character name could not be found from text " + text)
                pass

        # Convert all names to uppercase
        character_name = character_name.upper()

        return character_name

    def __check_multiple_characters(self):

        # Test for multiple character names in same line
        if (re.search("/",self.character)):
            multiple_characters = 1
        else:
            multiple_characters = 0

        return multiple_characters

    def __return_no_words(self):

        text = self.cleaned_text
        count = len(re.findall("\w+",text))

        return count

    def __cleaned_text(self):

        text = self.text
        cleaned_text = text.replace(self.character,"")

        return cleaned_text

    def __avg_sentence_legth(self):

        word_count = self.no_words
        no_full_stops = len(re.findall("\w(\.)+\s",self.text)) # Looks for full stop with letter in fornt and word after
        no_question_marks = len(re.findall("\w(\?)+\s",self.text))
        exclmation_marks = len(re.findall("\w(\!)+\s",self.text))
        exclmation_and_question = len(re.findall("\w((\!)+(\?)+)+\s",self.text))
        question_and_exclmation = len(re.findall("\w((\?)+(\!)+)+\s",self.text))
        cut_off = len(re.findall("\w((\-$)+)+\s",self.text))

        punctuation_stops = no_full_stops + no_question_marks + exclmation_marks + exclmation_and_question + question_and_exclmation + cut_off

        if punctuation_stops != 0:
            self.avg_setenece_length = word_count / punctuation_stops
            # print(self.text, self.avg_setenece_length)
        else:
            self.avg_setenece_length = word_count

        return self.avg_setenece_length

    def add_speech_count(self,speech_count_in):

        self.speech_count = speech_count_in

class Discription(TextBasedSection):

    def __init__(self,text,count):

        self.text = text
        self.count = count
        # No of words
        self.no_words = self.__return_no_words()

        # Sentiment analysis averaged for section and returned.
        self.sentiment = self.sentiment_analytis_text(self.text)

    def __return_no_words(self):

        text = self.text
        count = len(re.findall("\w+",text))

        return count

    def __repr__(self):
        return "Discription object form " + str(self.count) + "% way through the movie"

class Scene_change:

    def __init__(self,text,start_count,change_type):

        self.text = text
        self.start_count = start_count
        # Duplicate attriubte to make scene and speech more homegnous
        self.count = start_count
        # Change to outside => true = 1
        self.scene_change_to_outside = change_type
        # Values assigned using an setter function. Should be set in the following order
        self.finish_count = None
        self.speech_object_array = []
        self.description_object_array = []
        # Data dictionary => Built by function once all inputs have been collected
        self.scene_info_dict = {}

    def __repr__(self):
        return "Scene change at " + str(self.start_count) + "% through the script"

    # Functions to build information into scene
    def add_scene_finish_point(self,finish_count):

        self.finish_count = finish_count

    def add_object_array(self,speech_object_array,description_object_array):

        # Check that objects arrays are of the correct type or that array is empty
        assert len(speech_object_array) == 0 or type(speech_object_array[0]) == Speech
        assert len(description_object_array) == 0 or type(description_object_array[0]) == Discription

        self.speech_object_array = speech_object_array
        self.description_object_array = description_object_array

    # Use information to build a dict of information containted in scene.
    def build_data_dict(self):

        # Word analysis
        # Total / percentages
        total_speech = self.count_words_of_type_in_ob_array(type_speech=1)
        total_description = self.count_words_of_type_in_ob_array(type_description=1)
        total_words = total_speech + total_description
        # ensure no division by 0
        if total_words == 0:
            total_words = 1

        percent_speech = total_speech / total_words
        percent_description = total_description / total_words

        print("s",total_speech,"d",total_description,"t",total_words,"speech ",percent_speech,"descrip ",percent_description)

        # No of sections
        no_speech_sections = len(self.speech_object_array)
        no_description_sections = len(self.description_object_array)
        print("s",no_speech_sections,"d",no_description_sections)

        # List of
        list_of_characters = []
        characters_in_scene_dict = {}
        # Cycle through object array getting character names and add name if not already in list
        all_speech_in_scene = total_speech
        for ob in self.speech_object_array:
            character_name = ob.character
            # Percentage of words in scene
            no_words = ob.no_words
            percentage_scene_speech = no_words / all_speech_in_scene
            section_sentiment = ob.sentiment

            # Check if name in dict. If not add it and add other variables
            if characters_in_scene_dict.get(character_name):
                # Find dict in master character dict. Assign to var and then update all values
                current_sub_dict = characters_in_scene_dict.get(character_name)
                # Update values
                current_sub_dict["sections"] += 1
                current_sub_dict["no_words"] += no_words
                current_sub_dict["scene_percentage"] += percentage_scene_speech
                current_sub_dict["sentiment_array"].append(section_sentiment)

            else:
                # Not in dict. Create new sub dict and add first values in.
                characters_in_scene_dict[character_name] = {"name":character_name,"sections":1,"no_words":no_words,"scene_percentage":percentage_scene_speech,"sentiment_array":[section_sentiment]}


        print(characters_in_scene_dict, "\n")
        top_five_characters_in_scene = {}

        # Sentiment of section
        speech_sentiment = 0
        description_sentiment = 0
        overall_sentiment = 0

        # Scene type => mixed / only description - imply cut scene
        scene_only_description = 0

        # Scene type => mono / duo / tri / multi
        scene_interaction_type = ""

        # Sentence length for speech
        average_speech_sentence_length = 0

        # Language analysis


        pass

    def count_words_of_type_in_ob_array(self,type_description=0,type_speech=0):

        total_count = 0

        if type_description == 1:
            search_array = self.description_object_array
        elif type_speech == 1:
            search_array = self.speech_object_array
        else:
            search_array = []

        # Check array is set and greater then 0. Count no of words in array
        if len(search_array) > 0:
            total_count = 0
            for ob in search_array:
                number_of_words = ob.no_words
                total_count += number_of_words

        return total_count

    def return_string_words_in_ob_array(self,ob_array):

        word_string = ""

        for ob in ob_array:
            word_string += ob.text

        return word_string



if __name__ == '__main__':

    des = Discription("""  Coach Harvey pulls the Players apart just as the gym doors
          burst open.""",0.5)
    spe = Speech("""  MIKE
                    The best choice I ever made was
                    you.""",0.5)
    spe_2 = Speech("""  MIKE
                    The best choice I ever made was
                    you.""",0.5)
    spe_1 = Speech("""  SCARLET
                    What took you so long?""",0.5)
    spe_3 = Speech("""  MIKE
                    What took you so long?""",0.5)


    scene = Scene_change(" INT. FITCH SENIOR HIGH SCHOOL/TUNNEL - NIGHT",0.5,0)

    scene.add_scene_finish_point(0.6)
    scene.add_object_array([spe,spe_1,spe_2,spe_3],[des,des])



    scene.build_data_dict()