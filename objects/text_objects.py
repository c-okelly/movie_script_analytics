# Author Conor O'Kelly

# from vaderSentiment.vaderSentiment import sentiment as VS
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

# Generalised analytsis functions # Abstract function
class TextBasedScetion:

    def check_inheritance(self):
        print("hi")

    # Take text and return sentiment
    def sentiment_analytis_text(self,text_insert):

        text = text_insert

        token_text = tokenize.sent_tokenize(text)
        sid = SentimentIntensityAnalyzer()

        over_all_sentimnet = 0
        count = 0

        for sentence in token_text:
            score = sid.polarity_scores(sentence)
            # Create over all sentiment score
            over_all_sentimnet += score.get("compound")

            # If sentence is not neuteral add to sentence count for average
            if (score.get("compound") >  0.1):
                count += 1

        # Calculate average sentiment
        if count > 0:
            average_sentiment = over_all_sentimnet/count
        else:
            average_sentiment = over_all_sentimnet

        return average_sentiment

class Speech(TextBasedScetion):

    def __init__(self,text,count):

        ## Should add average length of line

        self.text = text
        self.count = count
        self.speech_count = 0
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
        self.sentimnet = self.sentiment_analytis_text(self.cleaned_text)
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

class Discription(TextBasedScetion):

    def __init__(self,text,count):

        self.text = text
        self.count = count
        # Sentiment analysis averaged for section and returned.
        self.sentimnet = self.sentiment_analytis_text(self.text)

    def __repr__(self):
        return "Discription object form " + str(self.count) + "% way through the movie"

class Scene_change:

    def __init__(self,text,start_count,change_type):

        self.text = text
        self.start_count = start_count
        # Duplicate attriubte to make scene and speech more homegnous
        self.count = start_count
        self.scene_change_to_outside = change_type
        # Values assigned using an setter function. Should be set in the following order
        self.finish_count = None
        self.objects_in_scene = []

    def __repr__(self):
        return "Scene change at " + str(self.start_count) + "% through the script"

    # Functions to build information into scene
    def add_scene_finish_point(self,finish_count):

        self.finish_count = finish_count

    def add_object_array(self,object_array):

        self.objects_in_scene = object_array



if __name__ == '__main__':

    text_ob = Discription("""  Coach Harvey pulls the Players apart just as the gym doors
          burst open. ED FREEDMAN, 17, sporting a jacket over a WIZARD
          costume, runs in, trips on his robe, gets up, peels his
          clothes off.""",0.5)

    print(text_ob.sentimnet)