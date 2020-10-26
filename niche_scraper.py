from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd 

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36")
opts.add_argument("--incognito")
capabilities = webdriver.DesiredCapabilities.CHROME

PROXY = "51.81.84.238:8080"
prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.autodetect = False
prox.http_proxy = PROXY
prox.ssl_proxy = PROXY
prox.add_to_capabilities(capabilities)

driver = webdriver.Chrome("./chromedriver", chrome_options=opts, desired_capabilities=capabilities)

data = {}

for i in range(5, 30):
    driver.get("https://www.niche.com/colleges/search/top-party-schools/?page=" + str(i))
    content = driver.page_source
    soup = BeautifulSoup(content)

    for section in soup.findAll('section', attrs={'class', 'search-result'}):
        name = section.find('h2',  attrs={'class', 'search-result__title'}).text
        rank = section.find('div', attrs={'class', 'search-result-badge'}).text.split(' ')[0][1:]

        all_grades = section.findAll('figure', attrs={'class', 'search-result-grade'})
        grade = "n/a"
        for figure in all_grades:
            if figure.find('figcaption', attrs={'class', 'search-result-grade__label'}).text == "Party Scene":
                grade = figure.find('div', attrs={'class', 'niche__grade'}).text

        data[name] = (rank, grade)

CSV ="\n".join([k+','+','.join(v) for k,v in data.items()])
with open("party-schools-niche.csv", "a") as file:
    file.write(CSV)

driver.quit()