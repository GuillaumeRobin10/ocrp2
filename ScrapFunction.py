import requests
from bs4 import BeautifulSoup
import urllib.request
import os

# make a directory
def make_a_dir(name,name2="",name3=""):
    try:
        os.mkdir(name+name2+name3)
    except FileExistsError:
        pass

#scrap categories from a html page and return an array
def make_categories_array(page):
    page_html= make_a_request(page)
    num_categories = page_html.find('div', {"class": "side_categories"}).find("ul", {"class": ""}).text
    categories = num_categories.replace("\n", ",").replace(" ", "-").replace("--", "").replace(",,", "").lower().split(",")
    return categories


#make a request
def make_a_request(page):
    return BeautifulSoup(requests.get(page).text, 'lxml')

# transform a character array into a string
def transform_array_into_a_string(start, end, array):
    string = ""
    index = start
    while index < end:
        string = string + array[index]
        index += 1
    return string


# case of 5
def case_of_star(star_number_string):
    if star_number_string == "One":
        return 1
    elif star_number_string == "Two":
        return 2
    elif star_number_string == "Three":
        return 3
    elif star_number_string == "Four":
        return 4
    elif star_number_string == "Five":
        return 5
    else:
        return 0


# return the number of page
def page_number(page):
    page_html= make_a_request(page)
    try:
        page_number_sting = page_html.find('li', {"class": "current"}).text.strip().replace(" ", "")
        number_of_pages = ""
        index = page_number_sting.find("of") + 2
        for browse_row in range(len(page_number_sting) - index):
            number_of_pages = number_of_pages + page_number_sting[index + browse_row]
        try:
            return int(number_of_pages)
        except TypeError:
            return 0
    except AttributeError:
        return 0


# get book's trait
def scrap_a_book_page(book_page, category):
    book_html = make_a_request(book_page)
    try:
        description = book_html.find('article', {"class": "product_page"}).find("p", {"class": ""}).text.replace("â", "'")
    except AttributeError:
        description = "scrapping error"
    try:
        title = book_html.find('div', {"class": "col-sm-6 product_main"}).find("h1", {"class": ""}).text.replace("â", "'")
    except AttributeError:
        title = "scrapping error"
        pass
    try:
        picture = str(book_html.find('div', {"class": "carousel-inner"})).strip().replace(" ", "").replace("\n", "")
        start_index_picture = picture.find("src=") + 11
        end_index_picture = picture.find(".jpg") + 4
        url_image = transform_array_into_a_string(start_index_picture, end_index_picture, picture)
    except AttributeError:
        url_image = "scrapping error"
    try:
        data = book_html.find('table', {"class": "table table-striped"}).text.strip().replace(" ", "").replace("\n", "")
        index_upc = data.find("UPC") + 3
        index_product_type = data.find("ProductType")
        index_price_exc_tax = data.find("Price(excl.tax)") + 16
        index_price_inc_tax = data.find("Price(incl.tax)") + 16
        index_tax = data.find("Tax")
        index_available = data.find("available")
        index_in_stock = data.find("Instock") + 8
        price_exc_tax = transform_array_into_a_string(index_price_exc_tax, index_price_inc_tax - 16, data)
        price_inc_tax = transform_array_into_a_string(index_price_inc_tax, index_tax, data)
        value_upc = transform_array_into_a_string(index_upc, index_product_type, data)
        if not index_in_stock == 7:
            stock = transform_array_into_a_string(index_in_stock, index_available, data)
        else:
            stock = 0

    except AttributeError:
        price_exc_tax = "scrapping error"
        price_inc_tax = "scrapping error"
        value_upc = "scrapping error"
        stock = "scrapping error"
    try:
        star_str = str(book_html.find('div', {"class": "col-sm-6 product_main"})).strip().replace(" ", "").replace("\n",
                                                                                                                   "")
        index_star = star_str.find("star-rating") + 11
        end_index_star = star_str.find('<iclass="icon-star">') - 2
        star_nub = transform_array_into_a_string(index_star, end_index_star, star_str)
        star = case_of_star(star_nub)
    except AttributeError:
        star = 0

    if title.find("/"):
        title = title.replace("/", "-")
    else:
        pass

    with open(f"results/{category}/{category}.csv", "a") as out_files2:
        out_files2.write(
            f"{book_page}|{value_upc}|{title}|{price_inc_tax}|{price_exc_tax}|{stock}|{description}|{category}|{star}|https://books.toscrape.com/{url_image}")
        out_files2.write("\n")
    urllib.request.urlretrieve("https://books.toscrape.com/" + url_image,
                               "results/" + category + "/image/" + title + ".jpg")

# return an array of book's url
def url_array(category_url_page):
    links = []
    num_of_pages = page_number(category_url_page) + 1
    if not num_of_pages == 1:
        for index in range(num_of_pages):
            page_url = category_url_page.replace("index.html", "") + "page-" + str(index) + ".html"
            soup = requests.get(page_url)
            articles = BeautifulSoup(soup.text, 'lxml').findAll("article")
            for index2 in articles:
                a = index2.find('a')
                link = a["href"]
                link = link.replace("../", "")
                links.append("http://books.toscrape.com/catalogue/" + link)
    else:
        page_url = category_url_page
        soup = requests.get(page_url)
        articles = BeautifulSoup(soup.text, 'lxml').findAll("article")
        for index2 in articles:
            a = index2.find('a')
            link = a["href"]
            link = link.replace("../", "")
            links.append("http://books.toscrape.com/catalogue/" + link)
    return links

def generate_csv(url, category):
    urls_array = url_array(url)
    for book in urls_array:
        scrap_a_book_page(book, category)


