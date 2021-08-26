import requests
import pandas as pd
from bs4 import BeautifulSoup


### fonction pour recuperer les categories et les liens ###
def rec_categories_livres(url_page):
    reponse_url_page = requests.get(url_page)
    if reponse_url_page.ok:
        soup = BeautifulSoup(reponse_url_page.text, 'html.parser')
        selection_categories = soup.find('ul', {'class': 'nav nav-list'}).find('ul').select('li')
        response = []
        for categorie in selection_categories:
            lien_categorie = 'http://books.toscrape.com/' + categorie.a['href']
            cat = (" ".join(categorie.get_text().split()), lien_categorie)
            response.append(cat)
        return response

## Fonction pour récupérer les urls pages de livres
def get_books(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup('article')
        for book in books:
            book_href = book.find('a')
            href = book_href['href']
            split = href.split('../')
            href = split[3]
            url_article = 'http://books.toscrape.com/catalogue/' + str(href)
            print (url_article)

    # tester si soup.find('section').find('li', {'class': 'next'}).select('a')
            page_suivante_lien = soup.find('section').find('li', {'class': 'next'}).select('a')
            print(page_suivante_lien)

    #ouvrir l'url et récupérer l'ensemble des livres de la page 2

if __name__ == '__main__':
    url_page = 'http://books.toscrape.com/index.html'
    categories_liens_df = pd.DataFrame(rec_categories_livres(url_page), columns= ['categorie','lien'])
    for url in categories_liens_df.lien:
        #print(url)
        get_books(url)


        #get_books (categories_liens_df.lien.iloc[index])

