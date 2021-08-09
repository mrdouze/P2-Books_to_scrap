import requests
from bs4 import BeautifulSoup


### Frecuperer les categories et les liens ###
def rec_categories_livres():

    url_page = 'http://books.toscrape.com/index.html'
    reponse_url_page = requests.get(url_page)
    soup = BeautifulSoup(reponse_url_page.text, 'html.parser')
    selection_categories = soup.find('ul', {'class': 'nav nav-list'}).find('ul').select('li')

    for categorie in selection_categories:
            lien_categorie = 'http://books.toscrape.com/' + categorie.a['href']
            print(categorie.get_text().split(),lien_categorie)

rec_categories_livres()
