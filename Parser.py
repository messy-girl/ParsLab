from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from openpyxl import Workbook
def parse():
    #раработает через раз: млсн тоже капчу кидает
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Квартиры"
    sheet.append(["Квартира", "Аресс", "Цена"])
    url = "https://omsk.mlsn.ru"

    headers = {'User-Agent': UserAgent().random}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    root = soup.find("div", id="root")
    page = root.find("div", class_="page")
    pagecontent = page.find("div", class_="page-content")
    homepage = pagecontent.find("div", class_="home-page")
    premium = homepage.find("div", class_="hexa-slider premium-announcement")
    content = premium.find("div", class_="hexa-slider__content")
    lowercontent = content.find("div", class_="hexa-slider__page_wrp")
    morelowercontent = lowercontent.find("div", class_="hexa-slider__page")
    row_content = morelowercontent.find("div", class_="row")
    while row_content:
        block_content = row_content.find("div", class_="announcement premium-item")

        while block_content:
            name = block_content.find("div", class_="type")
            address = block_content.find("div", class_="address")
            price = block_content.find("div", class_="price")


            sheet.append([name.text, address.text, price.text])

            block_content = block_content.next_sibling
        row_content = row_content.find_next_sibling("div", class_="row")

    workbook.save("table.xlsx")




