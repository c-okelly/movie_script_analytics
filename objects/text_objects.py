# Author Conor O'Kelly

# from vaderSentiment.vaderSentiment import sentiment as VS
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

class Speech:

    def __init__(self,text,count):

        ## Should add average length of line

        self.text = text
        self.count = count
        # Error message if character names can't be found
        self.errors_in_processing = 0
        self.error_message = ""
        # Set together
        self.character = self.__return_character_name()
        self.multiple_characters = self.__check_multiple_characters()
        # Sentiment analysis averaged for section and returned.
        self.sentimnet = self.__sentiment_analytis_text()
        self.no_words = self.__return_no_words()
        # Cleaned text version without character name
        self.cleaned_text = self.__cleaned_text()

    def __repr__(self):
        return "Speech object for character " + self.character + " from " + str(self.count) + "% through the script."

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

    def __sentiment_analytis_text(self):

        text = self.text
        # Strip character name from string
        text = text.replace(self.character,"")

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

    def __return_no_words(self):

        text = self.text
        count = len(re.findall("\w+",text))

        return count - 1

    def __cleaned_text(self):

        text = self.text
        cleaned_text = text.replace(self.character,"")

        return cleaned_text

class Discription:

    def __init__(self,text,count):

        self.text = text
        self.count = count

class Scene_change:

    def __init__(self,text,count,change_type):

        self.text = text
        self.count = count
        self.scene_change_to_outside = change_type

    def __repr__(self):
        return "Sceane change at " + str(self.count) + "% through the script"



if __name__ == '__main__':

    text_ob = Speech("""                              WENDY/James/John
                    Congratulations, Mike. You deserve
                    it. You're like a totally amazing
                    salesman.
                        """,0.5)

    print(text_ob.multiple_characters)