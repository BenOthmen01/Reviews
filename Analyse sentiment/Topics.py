import numpy as np

import pandas as pd
import seaborn as sns
from sklearn.utils import shuffle
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def importation(name):
       df=pd.read_csv(f"{name}", usecols=['title', 'rating', 'date', 'review',
              'CommentAferPreproc', 'sentiment'])
       #pour supprimer les # et mise en place de les données

       df["CommentAferPreproc"]= df["CommentAferPreproc"].str.lower()
       df["CommentAferPreproc"].fillna("",inplace=True)
       return df

#get the topics
df=importation("DataWithSentiment.csv")

cv = CountVectorizer(max_df=0.9, min_df=2)
dtm = cv.fit_transform(df["CommentAferPreproc"])
# dtm: 578 nombres d'article et 6842 les nombres des termes
LDA = LatentDirichletAllocation(n_components=7, random_state=42)
LDA.fit(dtm)
# Topics
single_topic = LDA.components_[0]
single_topic.argsort()  # get the location for a heighst value
# ARGSORT ==> INDEX POSITIONS SORTED FROM LEAST  TO GREATEST
# top 10 values (10 greatest values)
# last 10 values of argsort()
single_topic.argsort()[-10:]
top_ten_words = single_topic.argsort()[-10:]
for index in top_ten_words:
       print(cv.get_feature_names()[index])

for i, topic in enumerate(LDA.components_):
       print(f"les meilleures 7 sujets #{i}")
       print([cv.get_feature_names()[index] for index in topic.argsort()[-10:]])
       print('\n')
       print('\n')

topic_results=LDA.transform(dtm)
topic_results.argmax(axis=1)
df["Topic"]=topic_results.argmax(axis=1)
mytopic_dict={0:"service",1:"frais",2:"frais",3:"service",4:"service",5:"personnel",6:"accueil",7:"personnel"}
df["Topic_label"]=df["Topic"].map(mytopic_dict)

df.to_csv("DataWithSentiment_Topics.csv")
def split_dataFrame(df):
       g=df.groupby('title')
       for title, title_df in g:
              #print(title)
              #print(title_df)
              for i in range(len(title_df)):
                     title_df.to_csv(r"C:\Users\ibenothme\PycharmProjects\Reviews\Data"+"\ "+str(title)+".csv")
split_dataFrame(df)
