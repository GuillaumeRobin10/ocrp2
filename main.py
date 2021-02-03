from ScrapFunction import *
# init
HTTP_ROOT = "https://books.toscrape.com/catalogue/category/books/"
HTTP_END = "/index.html"
HOMEPAGE = "https://books.toscrape.com/"
HEADER = "product_page_url|universal_product_code(upc)|title|price_including_tax|price_excluding_tax|number_available|product_description|category|review_rating|image_url \n"
# end init


make_a_dir("results")
pageHtml= make_a_request(HOMEPAGE)
num_categories = pageHtml.find('div', {"class": "side_categories"}).find("ul", {"class": ""}).text
categories = num_categories.replace("\n", ",").replace(" ", "-").replace("--", "").replace(",,", "").lower().split(",")
category_length = len(categories)

for i in range(category_length):
    homepages = f"{HTTP_ROOT}{categories[i]}_{i + 2}{HTTP_END}"
    print(homepages)
    try:
        os.mkdir("results/"+categories[i])
        os.mkdir("results/"+categories[i]+"/image/")
    except FileExistsError:
        pass

    with open(f"results/{categories[i]}/{categories[i]}.csv", "w") as out_files:
        out_files.write(HEADER)
    generate_csv(homepages, categories[i])
