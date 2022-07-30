import requests
from bs4 import BeautifulSoup
import re
import  pandas as pd

url='https://www.hellomonnaie.fr/prestataire/categorie/banque/'
#url="https://www.hellomonnaie.fr/prestataire/floa-bank/avis/"
reviewlist=[]

def get_links(url):
    links=[]
    response = requests.get(url)
    if response.ok :
        soup=BeautifulSoup(response.text,'lxml')
        # pour avoir les elements qui fini avec /avis
        for ele in soup.find_all('a',href=re.compile("/avis")):
            links.append("https://www.hellomonnaie.fr"+ele.get('href'))
        return links
print(get_links(url))


def get_soup(url):
    response = requests.get(url)
    if response.ok :
        soup=BeautifulSoup(response.text,'lxml')
    return soup

def get_review(soup):

    reviews=soup.find_all('div',class_='review')
    try:
        for item in reviews:

            review={
                'title' : item.find('div', class_='title').text.strip(),
                'rating' : item.find('span', class_='rating-x-of-y').text.strip(),
                'date' : item.find('span', class_='desktop').text.strip(),
                'review' : item.find('div', class_='review-text').text.strip()

            }
            reviewlist.append(review)
    except:
        pass

soup=get_soup(url)
get_review(soup)
#print(len(reviewlist))

#parcourir tout les banques :
def Get_review_from_hellomonnaie(url):
    listes=get_links(url)
    adresse = []
    Titre=[]
    for row in listes:
        html_text=requests.get(str(row)).text
        soup=BeautifulSoup(html_text,"lxml")
        reviews=soup.find_all('div',class_='review')
        for item in reviews:
            review = {
                'title': item.find('div', class_='title').text.strip(),
                'rating': item.find('span', class_='rating-x-of-y').text.strip(),
                'date': item.find('span', class_='desktop').text.strip(),
                'review': item.find('div', class_='review-text').text.strip()

            }

            reviewlist.append(review)
            df=pd.DataFrame.from_records(reviewlist)
    return df.to_csv("hellomonnaie.csv")


#Get_review_from_hellomonnaie(url)
