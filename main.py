import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import os

### fonction pour recuperer les categories et les liens catégories###
def rec_categories_livres(url_page):
    #chrono = datetime.datetime.now()
    #print('rec_categorie_livres ', chrono)
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

## Fonction pour recuperer les infos livres ##
def get_book_details(url_book):
    #chrono = datetime.datetime.now()
    #print('get_book_details ', chrono)
    book_page = requests.get(url_book)
    soup = BeautifulSoup(book_page.text, 'html.parser')
    product_page_url = url_book
    title_selector = soup.find('head').text.split('|')
    title_selector = title_selector[0]
    title = title_selector.split('\n\n')[1]
    #print('title ', title)
    article_upc = str(soup.find('table', {'class': 'table table-striped'}).select('td')[0].text)
    #print('upc ',article_upc)
    price_excluding_tax = str(soup.find('table', {'class': 'table table-striped'}).select('td')[2].text)
    #print('price_excluding_tax ', price_excluding_tax)
    price_including_tax = str(soup.find('table', {'class': 'table table-striped'}).select('td')[3].text)
    #print('price_including_tax ', price_including_tax)
    number_available = str(soup.find('table', {'class': 'table table-striped'}).select('td')[5].text)
    #print('number_available ', number_available)
    product_description = str(soup.find('article', {'class': 'product_page'}).select('p')[3].text)
    category = str(soup.find('ul', {'class': 'breadcrumb'}).select('li')[2].text).replace("\n", '')
    #print(category)
    review_rating = soup.find('div', {'class': 'col-sm-6 product_main'}).select('p')[2]['class'][1]
    article_picture_selector = soup.find('div', {'class': 'item active'}).select('img')[0]['src']
    article_picture_split = article_picture_selector.split('../')[2]
    image_url = str('http://books.toscrape.com/' + article_picture_split)
    article_title = str(soup.find('div', {'class': 'col-sm-6 product_main'}).select('h1')[0].text)

    book_datas = {'product_page_url': product_page_url, 'upc': article_upc, 'title': article_title,
                  'price_including_tax': price_including_tax,
                  'price_excluding_tax': price_excluding_tax, 'number_available': number_available,
                  'product_description': product_description, 'category': category,
                  'review_rating': review_rating, 'image_url': image_url}
    return book_datas

### fonction pour télécharger les images
def get_book_picture(file_url, file_name, file_category):
    #chrono = datetime.datetime.now()
    #print('get_book_picture ', chrono)
    reponse = requests.get(file_url)
    try:
        os.mkdir('./images_livres')
    except Exception:
        pass
    if os.path.isdir('./images_livres/' + file_category):
        file_path = 'images_livres/' + file_category + '/' + file_name + '.' + file_url.split('.')[-1]
        with open(file_path, 'wb') as file:
            file.write(reponse.content)
    else:
        os.makedirs('./images_livres/' + file_category)
        file_path = 'images_livres/' + file_category + '/' + file_name + '.' + file_url.split('.')[-1]
        with open(file_path, 'wb') as file:
            file.write(reponse.content)

## Fonction pour récupérer les urls pages de livres
def get_books(url):
    #chrono = datetime.datetime.now()
    #print('get_books ', chrono)
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup('article')
        liste_liens_livres=[]
        for book in books:
            book_href = book.find('a')
            href = book_href['href']
            split = href.split('../')
            href = split[3]
            url_article = 'http://books.toscrape.com/catalogue/' + str(href)
            liste_liens_livres.append(get_book_details(url_article))

        page_suivante_lien = soup.find('section').find('li', {'class': 'next'})
        if page_suivante_lien is not None:
            page_suivante_lien = page_suivante_lien.select('a')[0]['href']
            new_url = "/".join(url.split("/")[:-1]) + "/" + page_suivante_lien
            liste_liens_livres += get_books(new_url)
        return liste_liens_livres

## fonction principale du programme
def main():
    #chrono = datetime.datetime.now()
    #print('main deb: ', chrono)

    url_page = 'http://books.toscrape.com/index.html'
    categories_liens_df = pd.DataFrame(rec_categories_livres(url_page), columns=['categorie', 'lien'])
    try:
        os.mkdir('./fichiers_csv')
    except Exception:
        pass
    for row in categories_liens_df.iterrows():
        url = row[1]['lien']
        category = row[1]['categorie']
        df = pd.DataFrame(get_books(url))
        df.to_csv("fichiers_csv/" + category + ".csv")
        df.apply(lambda r: get_book_picture(r["image_url"], r["upc"], category), axis=1)
    #chrono =datetime.datetime.now()
    #print('main fin: ',chrono)

## Lancement du programme
if __name__ == '__main__':
   main()
