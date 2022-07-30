import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import re
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
import string
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

nltk.download('stopwords')
df=pd.read_csv(r"C:\Users\ibenothme\PycharmProjects\Reviews\Review_Banque\hellomonnaie.csv",usecols=['title', 'rating', 'date', 'review'])

df["review"]= df["review"].str.lower()

def tokenization(df):
    #Word Tokenization and deleting punctuation
    AComment=[]
    for comment in df["review"].apply(str):
        Word_Tok = []
        for word in  re.sub("\W"," ",comment ).split():
            Word_Tok.append(word)
        AComment.append(Word_Tok)

    return AComment

def stop_word(df):

    #set of Spacy's default stop words and delete negation words

    stop_words=stopwords.words('french')

    deselect_stop_words = ['n\'','plus','personne','aucun','ni','aucune','rien']
    for w in deselect_stop_words:
        if w in stop_words:
            stop_words.remove(w)
        else:
            continue

    #suprimer les stop words

    AllfilteredComment=[]
    for comment in df["Word_Tok"]:
        filteredComment = [w for w in comment if not ((w in stop_words) or (len(w) == 1))]
        AllfilteredComment.append(' '.join(filteredComment))
    return AllfilteredComment


df["Word_Tok"]= tokenization(df)
df["CommentAferPreproc"]=stop_word(df)

def sentiement_analysis(df):
    #Sentiment Analysis with TextBlob

    senti_list = []
    for i in df["CommentAferPreproc"]:
        vs = tb(i).sentiment[0]
        if (vs > 0):
            senti_list.append('Positive')
        elif (vs < 0):
            senti_list.append('Negative')
        else:
            senti_list.append('Neutral')
    return senti_list

#**Add Column: Sentiment**

df["sentiment"]=sentiement_analysis(df)
df['title'] = df['title'].str.split('#').str[0]
df['date'] = df['date'].str.extract(r"(\d{1,2}[/. ](?:\d{1,2}|January|Jan)[/. ]\d{2}(?:\d{2})?)")

df.to_csv("DataWithSentiment.csv")









