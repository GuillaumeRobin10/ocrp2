from ScrapFunction import *
# init
HTTP_ROOT = "https://books.toscrape.com/catalogue/category/books/"
HTTP_END = "/index.html"
HOMEPAGE = "https://books.toscrape.com/"
HEADER = "product_page_url|universal_product_code(upc)|title|price_including_tax|price_excluding_tax|number_available|product_description|category|review_rating|image_url \n"
# end init
make_a_dir("results")
categories = make_categories_array(HOMEPAGE)
for i in range(len(categories)):
    homepages = f"{HTTP_ROOT}{categories[i]}_{i + 2}{HTTP_END}"
    print(homepages)
    make_a_dir("results/",categories[i])
    make_a_dir("results/", categories[i],"/image/")
    with open(f"results/{categories[i]}/{categories[i]}.csv", "w") as out_files:
        out_files.write(HEADER)
    generate_csv(homepages, categories[i])