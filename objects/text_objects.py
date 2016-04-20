# Author Conor O'Kelly

# from vaderSentiment.vaderSentiment import sentiment as VS
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

class Discription:

    def __init__(self,text,count):

        self.text = text
        self.count = count

class Speech:

    def __init__(self,text,count):

        self.text = text
        self.count = count
        self.character = self.return_character_name()
        self.sentimnet = self.sentiment_analytis_text()
        self.no_words = self.return_no_words()

    def return_character_name(self):

        text = self.text

        character_name = text.split("\n")[0]

        character_name = character_name.strip()

        return character_name

    def sentiment_analytis_text(self):

        text = self.text

        token_text = tokenize.sent_tokenize(text)
        sid = SentimentIntensityAnalyzer()

        over_all_sentimnet = 0
        for sentence in token_text:
            # print(sentence)
            score = sid.polarity_scores(sentence)
            # print(score)
            over_all_sentimnet += score.get("compound")
        # print(over_all_sentimnet/10)

    def return_no_words(self):

        text = self.text
        count = len(re.findall("\w+",text))

        return count


class Scene_change:

    def __init__(self,text,count):

        self.text = text
        self.count = text




if __name__ == '__main__':

    text_ob = Speech("""                              WENDY
                    Congratulations, Mike. You deserve
                    it. You're like a totally amazing
                    salesman.
                        """,0.5)

    print(text_ob.no_words)