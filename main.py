import requests
from bs4 import BeautifulSoup
import urllib.request
import os


# construit un chaine de caractere avec un table , un indexmin et un indexmax
def scrapdata(indexstart, maxindex, info):
    data = ""
    index = indexstart
    while index < maxindex:
        data = data + info[index]
        index += 1
    return data


# case of 5
def caseofstar(starNubStr):
    if starNubStr == "One":
        return 1
    elif starNubStr == "Two":
        return 2
    elif starNubStr == "Three":
        return 3
    elif starNubStr == "Four":
        return 4
    elif starNubStr == "Five":
        return 5
    else:
        print("erreur")
        return 9


# scrap les données de la page d'un livre
def scrapABook(bookPage, categorie):
    Home = requests.get(bookPage)
    pageHtml = BeautifulSoup(Home.text, 'lxml')
    article = pageHtml.find('article', {"class": "product_page"})
    try:
        description = article.find("p", {"class": ""}).text
    except:
        description="none"

    titreBal = pageHtml.find('div', {"class": "col-sm-6 product_main"})
    titre = titreBal.find("h1", {"class": ""}).text
    imageBal = pageHtml.find('div', {"class": "carousel-inner"})
    image = str(imageBal)
    image = image.strip().replace(" ", "")
    image = image.strip().replace("\n", "")
    indexImagelink = image.find("src=") + 11
    endIndexImagelink = image.find(".jpg") + 4
    datas = pageHtml.find('table', {"class": "table table-striped"}).text
    datas = datas.strip().replace(" ", "")
    datas = datas.strip().replace("\n", "")
    indexUPC = datas.find("UPC") + 3
    indexProductType = datas.find("ProductType")
    indexPriceExcTax = datas.find("Price(excl.tax)") + 16
    indexPriceIncTax = datas.find("Price(incl.tax)") + 16
    indexTax = datas.find("Tax")
    indexAvailable = datas.find("available")
    indexInStock = datas.find("Instock") + 8
    starStr = str(titreBal).strip().replace(' ', "").replace('\n', '')
    indexStar = starStr.find("star-rating") + 11
    endindexStar = starStr.find('<iclass="icon-star">') - 2
    starnub = scrapdata(indexStar, endindexStar, starStr)
    star = caseofstar(starnub)
    if not indexInStock == 7:
        stock = scrapdata(indexInStock, indexAvailable, datas)
    else:
        stock = 0
    upc = scrapdata(indexUPC, indexProductType, datas)
    priceExcTax = scrapdata(indexPriceExcTax, indexPriceIncTax - 16, datas)
    priceIncTax = scrapdata(indexPriceIncTax, indexTax, datas)
    urlImage = scrapdata(indexImagelink, endIndexImagelink, image)

    with open(f"{categorie}/{categorie}.csv", "a") as outfiles:
        outfiles.write(f"{bookPage}|{upc}|{titre}|{priceIncTax}|{priceExcTax}|{stock}|{description} |{categorie}|{star}|https://books.toscrape.com/{urlImage}")
        outfiles.write("\n")
    if titre.find("/"):
        titre = titre.replace("/","-")
    else:
        pass

    urllib.request.urlretrieve("https://books.toscrape.com/"+urlImage,categorie+"/image/"+titre+".jpg")

# scrap le nb de pages aucun vérification
def nb_page(Homepage):
    Home = requests.get(Homepage)
    pageHtml = BeautifulSoup(Home.text, 'lxml')
    try:
        nbPage_str = pageHtml.find('li', {"class": "current"}).text.strip().replace(" ", "")
        maxvalue = ""
        index = nbPage_str.find("of")
        indexI = index + 2
        maxi = len(nbPage_str)
        for i in range(maxi - indexI):
            maxvalue = maxvalue + nbPage_str[indexI + i]
        return int(maxvalue)
    except:
        return 0

    # récupération de l'url des livres


# return an array of article's url
def urlArray(categorieUrlPage):
    links = []
    nombrePage = nb_page(categorieUrlPage) + 1
    if not nombrePage == 1:
        for i in range(nombrePage):
            pagess = categorieUrlPage.replace("index.html","")
            page = pagess + "page-" + str(i) + ".html"
            soup = requests.get(page)
            pageEn = BeautifulSoup(soup.text, 'lxml')
            articles = pageEn.findAll("article")

            for i in articles:
                a = i.find('a')
                link = a["href"]
                link = link.replace("../", "")
                links.append("http://books.toscrape.com/catalogue/" + link)
    else:
        page = categorieUrlPage
        soup = requests.get(page)
        pageEn = BeautifulSoup(soup.text, 'lxml')
        articles = pageEn.findAll("article")
        for i in articles:
            a = i.find('a')
            link = a["href"]
            link = link.replace("../", "")
            links.append("http://books.toscrape.com/catalogue/" + link)

    return links
    ### on as tous les liens dans links.g


def generateCsv(url, categorie="travel"):
    urlsArrays = urlArray(url)
    for book in urlsArrays:
        scrapABook(book, categorie)


Homepage = "https://books.toscrape.com/"
Home = requests.get(Homepage)
pageHtml = BeautifulSoup(Home.text, 'lxml')
nbPage_str = pageHtml.find('div', {"class": "side_categories"})
nbcat = nbPage_str.find("ul", {"class": ""}).text
categories = nbcat.replace("\n", ",")
categories = categories.replace(" ", "-")
categories = categories.replace("--", "")
categories = categories.replace(",,", "")
categories = categories.lower()
categories = categories.split(",")
httpRacine = "https://books.toscrape.com/catalogue/category/books/"
httpEnd = "/index.html"
y = len(categories)

for i in range(y):
    homepages = (f'{httpRacine}{categories[i]}_{i + 2}{httpEnd}')
    print(homepages)
    try:
        os.mkdir(categories[i])
        os.mkdir(categories[i]+"/image/")
    except:
        pass

    with open(f"{categories[i]}/{categories[i]}.csv", "a") as outfiles:
        outfiles.write("product_page_url|universal_product_code(upc)|title|price_including_tax|price_excluding_tax|number_available|product_description|category|review_rating|image_url \n")
    generateCsv(homepages, categories[i])
