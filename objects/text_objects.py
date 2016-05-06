# Author Conor O'Kelly

# from vaderSentiment.vaderSentiment import sentiment as VS
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
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

    def return_language_analysis_dict(self,string_to_be_analysed):

        language_dict = {}

        ### Change if no default tagger used. Info available higher up!
        language_dict["pos_tagger_used"] = "default_nltk_tagger => Penn Treebank"

        # Tokenize text
        token_text = nltk.word_tokenize(string_to_be_analysed)
        token_text = nltk.pos_tag(token_text)

        # Catagories of words => nouns / verb / adjective / adverb / pronouns / modal /
        for tagged_word in token_text:
            if language_dict.get(tagged_word[1]):
                language_dict[tagged_word[1]] += 1
            else:
                language_dict[tagged_word[1]] = 1

        # print(token_text, "\n")
        # print(nltk.help.upenn_tagset())

        # # Add subdict with key explanations
        # key_explanations = {'CC':'Coordinating conjunction'},{'CD':'Cardinal number'},{'DT':'Determiner'},{'EX':'Existential there'},{'FW':'Foreign word'},{'IN':'Preposition or subordinating conjunction'},{'JJ':'Adjective'},{'JJR':'Adjective, comparative'},{'JJS':'Adjective, superlative'},{'LS':'List item marker'},{'MD':'Modal'},{'NN':'Noun, singular or mass'},{'NNS':'Noun, plural'},{'NNP':'Proper noun, singular'},{'NNPS':'Proper noun, plural'},{'PDT':'Predeterminer'},{'POS':'Possessive ending'},{'PRP':'Personal pronoun'},{'PRP$':'Possessive pronoun'},{'RB':'Adverb'},{'RBR':'Adverb, comparative'},{'RBS':'Adverb, superlative'},{'RP':'Particle'},{'SYM':'Symbol'},{'TO':'to'},{'UH':'Interjection'},{'VB':'Verb, base form'},{'VBD':'Verb, past tense'},{'VBG':'Verb, gerund or present participle'},{'VBN':'Verb, past participle'},{'VBP':'Verb, non-d person singular present'},{'VBZ':'Verb, d person singular present'},{'WDT':'Wh-determiner'},{'WP':'Wh-pronoun'},{'WP$':'Possessive wh-pronoun'},{'WRB':'Wh-adverb'}
        # language_dict["key_explanations"] = key_explanations

        return language_dict


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
        self.avg_sentence_length = self.__avg_sentence_legth()

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
            self.avg_sentence_length = word_count / punctuation_stops
            # print(self.text, self.avg_sentence_length)
        else:
            self.avg_sentence_length = word_count

        return self.avg_sentence_length

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

class Scene_change(TextBasedSection):

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

        #### Word analysis ####
        ### Total / percentages
        total_speech = self.count_words_of_type_in_ob_array(type_speech=1)
        total_description = self.count_words_of_type_in_ob_array(type_description=1)
        total_words = total_speech + total_description
        # ensure no division by 0
        if total_words == 0:
            total_words = 1

        percent_speech = total_speech / total_words
        percent_description = total_description / total_words

        # print("s",total_speech,"d",total_description,"t",total_words,"speech ",percent_speech,"descrip ",percent_description)

        ### No of sections
        no_speech_sections = len(self.speech_object_array)
        no_description_sections = len(self.description_object_array)
        no_total_sections = no_speech_sections + no_description_sections
        # print("s",no_speech_sections,"d",no_description_sections)

        ### Scene type => mixed / only description - imply cut scene
        if no_speech_sections == 0 and no_description_sections > 0:
            scene_only_description = 1
        else:
            scene_only_description = 0

        ### Dict of characters in scene with data
        characters_in_scene_dict = self.__generate_character_in_scene_dict(total_speech)

        # Test print.
        # print(characters_in_scene_dict, "\n")

        ### Find top 10 characters in each scene
        # Cycle through dict. Create array of character_name and % in scene. Sort and take first 5
        top_ten_characters_in_scene = self.__find_top_10_character(characters_in_scene_dict)

        # print(top_ten_characters_in_scene)

        ### Sentiment of section
        # For each add all sentiments to array. Exclude 0 elements, take absolute values sum and divide by number left.

        # Speech
        speech_sentiment_array = []
        for obj in self.speech_object_array:
            if abs(obj.sentiment) > 0:
                speech_sentiment_array.append(obj.sentiment)
            else:
                pass
        # Sum and divide by no left. Set to zero
        try:
            speech_sentiment = sum(speech_sentiment_array) / len(speech_sentiment_array)
        except ZeroDivisionError:
            speech_sentiment = 0

        # Description
        description_sentiment_array = []
        for obj in self.description_object_array:
            if abs(obj.sentiment) > 0:
                description_sentiment_array.append(obj.sentiment)
            else:
                pass

        try:
            description_sentiment = sum(description_sentiment_array)/ len(description_sentiment_array)
        except:
            description_sentiment = 0

        # print(speech_sentiment,description_sentiment)

        # Overall sentiment
        overall_sentiment_array = []
        if abs(speech_sentiment) > 0:
            overall_sentiment_array.append(speech_sentiment)
        if abs(description_sentiment) > 0:
            overall_sentiment_array.append(description_sentiment)

        try:
            overall_sentiment = sum(overall_sentiment_array)/ len(overall_sentiment_array)
        except ZeroDivisionError:
            overall_sentiment = 0

        # print(speech_sentiment,description_sentiment,overall_sentiment)

        ### Scene type => mono / duo / tri / multi
        scene_interaction_dict = self.__determine_scene_interaction_type(top_ten_characters_in_scene)
        # print(scene_interaction_dict)

        ### Sentence length for speech
        average_sentence_length_array = []

        for scene_ob in self.speech_object_array:
            average_sentence_length_array.append(scene_ob.avg_sentence_length)
        try:
            average_speech_sentence_length = sum(average_sentence_length_array) / len(average_sentence_length_array)
        except ZeroDivisionError:
            average_speech_sentence_length = 0
        # print(average_speech_sentence_length)

        ### Language analysis
        # Get strings
        speech_string = self.return_string_words_in_ob_array(speech_array=1)
        description_string = self.return_string_words_in_ob_array(description_array=1)
        both_strings = speech_string + description_string
        # Use function from parent class to perform the analysis
        speech_language_dict = self.return_language_analysis_dict(speech_string)
        description_language_dict = self.return_language_analysis_dict(description_string)
        overall_lanaguage_dict = self.return_language_analysis_dict(both_strings)

        # Build scene_info_dict => from all variables above

        self.scene_info_dict = {"total_speech":total_speech,"total_description":total_description,"total_words":total_words,"percent_speech":percent_speech,
                                "percent_description":percent_description,"no_speech_sections":no_speech_sections,"no_description_sections":no_description_sections,
                                "no_total_sections":no_total_sections,"scene_only_description":scene_only_description,
                                "characters_in_scene_dict":characters_in_scene_dict,"top_ten_characters_in_scene":top_ten_characters_in_scene,
                                "speech_sentiment":speech_sentiment,"description_sentiment":description_sentiment,"overall_sentiment":overall_sentiment,
                                "scene_interaction_dict":scene_interaction_dict,"average_speech_sentence_length":average_speech_sentence_length,
                                "speech_language_dict":speech_language_dict,"description_language_dict":description_language_dict,
                                "overall_lanaguage_dict":overall_lanaguage_dict}

        return self.scene_info_dict

    def __determine_scene_interaction_type(self,top_characters_array):

        interaction_dict = {}
        if len(top_characters_array) > 0:
            # If more then 80 % => Single person
            if top_characters_array[0][1] > 0.8:
                interaction_dict["one_main_character"] = 1
                interaction_dict["two_main_character"] = 0
                interaction_dict["multiple_characters"] = 0
                interaction_dict["percentage_of_scene"] = top_characters_array[0][1]

            # If 2 combined more then 80 % => Two people
            elif len(top_characters_array) > 1 and (top_characters_array[0][1] + top_characters_array[1][1]) > 0.85:
                interaction_dict["one_main_character"] = 0
                interaction_dict["two_main_character"] = 1
                interaction_dict["multiple_characters"] = 0
                interaction_dict["percentage_of_scene"] = top_characters_array[0][1] + top_characters_array[1][1]
            # Else => multiple
            else:
                interaction_dict["one_main_character"] = 0
                interaction_dict["two_main_character"] = 0
                interaction_dict["multiple_characters"] = 1
                interaction_dict["percentage_of_scene"] = None

        else:
            interaction_dict["one_main_character"] = 0
            interaction_dict["two_main_character"] = 0
            interaction_dict["multiple_characters"] = 0
            interaction_dict["percentage_of_scene"] = None


        return interaction_dict

    def __find_top_10_character(self,characters_in_scene_dict):

        ### Find top 10 characters in each scene
        # Cycle through dict. Create array of character_name and % in scene. Sort and take first 5
        all_chars_array = []
        for char_dict_name in characters_in_scene_dict:
            current_dict_1 = characters_in_scene_dict.get(char_dict_name)
            character_info = [current_dict_1.get("name"), current_dict_1.get("scene_percentage")]
            all_chars_array.append(character_info)

        # Sort character array based on percentage of scene. So highest is first
        sorted_all_chars_array = sorted(all_chars_array, key=lambda x:x[1],reverse=True)

        # Take top 5 character from each scene if there is more then 10
        if len(sorted_all_chars_array)> 10:
            top_ten_characters_in_scene = sorted_all_chars_array[:10]
        else:
            top_ten_characters_in_scene = sorted_all_chars_array

        return top_ten_characters_in_scene

    def __generate_character_in_scene_dict(self,all_speech_in_scene):

        ### Dict of characters in scene with data
        characters_in_scene_dict = {}
        # Cycle through object array getting character names and add name if not already in list
        for ob in self.speech_object_array:
            character_name = ob.character
            # Percentage of words in scene
            no_words = ob.no_words

            try:
                percentage_scene_speech = no_words / all_speech_in_scene
            except ZeroDivisionError:
                # print(character_name)
                percentage_scene_speech = 0

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

        # Cycle through dicts and add new variable of averaged sentiment.
        # Add all variables and divide number of non zero ones.
        for char_dict in characters_in_scene_dict:
            current_dict = characters_in_scene_dict.get(char_dict)
            current_sentiment_array = current_dict.get("sentiment_array")
            # Add sentiments and get average
            avg_sentiment = 0
            no_non_zero_sentiments = 0
            total_of_sentiments = 0
            for sentiment_value in current_sentiment_array:
                if sentiment_value != 0:
                    no_non_zero_sentiments += 1
                # Add sentiment values together
                total_of_sentiments += sentiment_value

            # Get average sentiment and add to current dict. Prevent division by 0
            if no_non_zero_sentiments == 0:
                avg_sentiment = 0
            else:
                avg_sentiment = total_of_sentiments / no_non_zero_sentiments

            current_dict["average_sentiment"] = avg_sentiment

        return characters_in_scene_dict

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

    def return_string_words_in_ob_array(self,description_array=0,speech_array=0):

        word_string = ""

        # Set search arry
        if description_array == 1:
            search_array = self.description_object_array
            for ob in search_array:
                word_string += ob.text
        # Take cleaned text with no names
        elif speech_array == 1:
            search_array = self.speech_object_array
            for ob in search_array:
                word_string += ob.cleaned_text
        else:
            search_array = []
            word_string = "No array selected for search"


        return word_string

class TextWorker(TextBasedSection):
    ### Class used to access functions in class => TextBasedSection

    def __init__(self):
        pass

if __name__ == '__main__':

    des = Discription("""  Coach Harvey pulls the Players apart just as the gym doors
          burst open good.""",0.5)
    des_1 = Discription("""  Coach Harvey pulls the Players apart just as the gym doors
          burst open bad.""",0.5)

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


    # print(des_1.sentiment)
    scene = Scene_change(" INT. FITCH SENIOR HIGH SCHOOL/TUNNEL - NIGHT",0.5,0)

    scene.add_scene_finish_point(0.6)
    scene.add_object_array([spe,spe_1,spe_2,spe_3],[des,des_1])



    scene.build_data_dict()
    print(scene.scene_info_dict)