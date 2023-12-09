from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_product(search_query, all_goods, found_goods):
    for i in found_goods:
        image = i.find('div', {"class": 'grid-product__image-wrap'})
        img = image.find('img').get('src')
        title = i.find('div', {"class": 'grid-product__title-inner'}).text.strip()
        price = i.find('div', {"class": "grid-product__price-value ec-price-item"}).text.replace("\xa0", '')
        all_goods.append((search_query, title, price, img))
    return all_goods


def parse_website(search_query):
    all_goods = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword={search_query}')
    driver.implicitly_wait(10)
    html = driver.execute_script("return document.body.innerHTML")
    driver.close()
    bsObj = BeautifulSoup(html, 'html.parser')
    found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})
    number = int(bsObj.find('div', {"class": "ec-breadcrumbs"}).text.replace("Магазин/Поиск: нашлось ", ''))
    print(number)

    if number > 60 and number < 120:
        for i in range(0, 61, 60):
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword={search_query}&offset={i}')
            driver.implicitly_wait(10)
            html = driver.execute_script("return document.body.innerHTML")
            driver.close()
            bsObj = BeautifulSoup(html, 'html.parser')
            found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})
            all_goods = get_product(search_query, all_goods, found_goods)

    elif number > 120:
        for i in range(0, 121, 60):
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword={search_query}&offset={i}')
            driver.implicitly_wait(10)
            html = driver.execute_script("return document.body.innerHTML")
            driver.close()
            bsObj = BeautifulSoup(html, 'html.parser')
            found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})
            all_goods = get_product(search_query, all_goods, found_goods)

    else:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f'https://zielinskiandrozen.ru/magazin/search?keyword={search_query}')
        driver.implicitly_wait(10)
        html = driver.execute_script("return document.body.innerHTML")
        driver.close()
        bsObj = BeautifulSoup(html, 'html.parser')
        found_goods = bsObj.find_all('div', {'class': "grid-product__wrap-inner"})
        all_goods = get_product(search_query, all_goods, found_goods)
    
    return all_goods
