from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import time

def get_all_niche_party_schools():
    for i in range(1,65):
        driver = get_driver()
        niche_party_schools(driver, i)
        driver.quit()

def niche_party_schools(driver, i):
    data = {}

    driver.get("https://www.niche.com/colleges/search/top-party-schools/?page=" + str(i))
    content = driver.page_source
    soup = BeautifulSoup(content)

    for section in soup.findAll('section', attrs={'class', 'search-result'}):
        name = section.find('h2',  attrs={'class', 'search-result__title'}).text
        name = clean_name(name)
        rank = section.find('div', attrs={'class', 'search-result-badge'}).text.split(' ')[0][1:]

        all_grades = section.findAll('figure', attrs={'class', 'search-result-grade'})
        grade = "n/a"
        for figure in all_grades:
            if figure.find('figcaption', attrs={'class', 'search-result-grade__label'}).text == "Party Scene":
                grade = figure.find('div', attrs={'class', 'niche__grade'}).text

        data[name] = (rank, grade)

    CSV ="\n".join([k+','+','.join(v) for k,v in data.items()])
    with open("./data/party-schools-niche.csv", "a") as file:
        file.write(CSV)

def stacker_party_schools(driver):
    data = {}

    for i in range(1, 6):
        driver.get("https://stacker.com/stories/3217/top-50-party-schools-america?page=" + str(i))
        content = driver.page_source
        soup = BeautifulSoup(content)

        for div in soup.findAll('div', attrs={'class', 'slideshow-slide__title'}):
            name_and_rank = div.find('h2').text
            if name_and_rank[0] == "#":
                rank = name_and_rank.split(".")[0][1:]
                name = name_and_rank.split(".")[1][1:]
                name = clean_name(name)
                data[name] = (rank)

    CSV ="\n".join([k+','+ v for k,v in data.items()])
    with open("./data/party-schools-stacker.csv", "a") as file:
        file.write(CSV)

def bestcolleges_party_schools(driver):
    data = ""

    driver.get("https://www.bestcolleges.com/features/best-party-schools/")
    content = driver.page_source
    soup = BeautifulSoup(content)

    for tr in soup.findAll('tr', attrs={'class', 'js-ranking-row'}):
        rank = tr.find('td', attrs={'class', 'rank'}).text
        name = tr.find('td', attrs={'class', 'school'}).find('h3').text
        name = clean_name(name)
        data += name + "," + rank.strip() + "\n"

    with open("./data/party-schools-bestcolleges.csv", "a") as file:
        file.write(data)

def clean_name(name):
    return name.replace(",", "")

def translate_name_to_search_name(name):
    name = name.replace("&", "-and-")
    name = name.replace(',', '')
    name = name.replace('.', '')
    name = name.replace('(', '')
    name = name.replace(')', '')
    name = name.replace('\'', '')
    return name.replace(' ', '-').strip().lower()

def niche_details_data(driver, name):
    percent_female = "n/a"
    percent_male = "n/a"
    self_republican = "n/a"
    self_democratic = "n/a"
    self_indep = "n/a"
    self_other = "n/a"
    self_dont_care = "n/a"
    school_very_liberal = "n/a"
    school_liberal = "n/a"
    school_moderate = "n/a"
    school_conservative = "n/a"
    school_very_conservative = "n/a"
    school_libertarian = "n/a"
    school_not_sure = "n/a"

    search_name = translate_name_to_search_name(name)
    driver.get("https://www.niche.com/colleges/" + search_name + "/students/")
    content = driver.page_source
    soup = BeautifulSoup(content)

    # Percent male and female
    for div in soup.findAll('div', attrs={'class', 'scalar--three'}):
        label = div.find('div', attrs={'class', 'scalar__label'}).text
        if label == "Female Undergrads":
            div2 = div.find('div', attrs={'class', 'scalar__value'})
            if div2 != None:
                percent_female = div2.text
        elif label == "Male Undergrads":
            div2 = div.find('div', attrs={'class', 'scalar__value'})
            if div2 != None:
                percent_male = div2.text

    # Political affiliation
    for div in soup.findAll('div', attrs={'class', 'poll__table--bar_chart_color'}):
        label = div.find('div', attrs={'class', 'poll__table__body'}).text
        if label == "What political party do you associate yourself with?":
            for li in div.findAll('li', attrs={'class', 'poll__table__result__item'}):
                inner_label = li.find('div', attrs={'class', 'poll__table__result__label'})
                if inner_label == None:
                    continue
                inner_label = inner_label.text
                value = li.find('div', attrs={'class', 'poll__table__result__percent'}).text
                if inner_label == "Republican":
                    self_republican = value
                elif inner_label == "Democratic":
                    self_democratic = value
                elif inner_label == "Independent":
                    self_indep = value
                elif inner_label == "Other party not mentioned":
                    self_other = value
                elif inner_label == "I don\'t care about politics":
                    self_dont_care = value
        elif label == "How would you best describe the political beliefs of campus as a whole? ":
            for li in div.findAll('li', attrs={'class', 'poll__table__result__item'}):
                inner_label = li.find('div', attrs={'class', 'poll__table__result__label'})
                if inner_label == None:
                    continue
                inner_label = inner_label.text
                value = li.find('div', attrs={'class', 'poll__table__result__percent'}).text
                if inner_label == "Progressive/very liberal":
                    school_very_liberal = value
                elif inner_label == "Liberal":
                    school_liberal = value
                elif inner_label == "Moderate":
                    school_moderate = value
                elif inner_label == "Conservative":
                    school_conservative = value
                elif inner_label == "Very conservative":
                    school_very_conservative = value
                elif inner_label == "Libertarian":
                    school_libertarian = value
                elif inner_label == "Not sure":
                    school_not_sure = value
    return ",".join([name, percent_female, percent_male, self_republican, self_democratic, self_indep, self_other, self_dont_care, school_very_liberal, school_liberal, school_moderate, school_conservative, school_very_conservative, school_libertarian, school_not_sure])

def get_all_niche_details_data():
    df = pd.read_csv("./data/party-schools-niche.csv")

    CSV_header = "Name, percent_female, percent_male, self_republican, self_democratic, self_indep, self_other, self_dont_care, school_very_liberal, school_liberal, school_moderate, school_conservative, school_very_conservative, school_libertarian, school_not_sure\n"
    with open("./data/details-data-niche.csv", "a") as file:
        file.write(CSV_header)

    for index, row in df.iterrows():
        print(index)
        name = row['Name']
        driver = get_driver()
        data = niche_details_data(driver, "The Los Angeles Film School")
        driver.quit()
        with open("./data/details-data-niche.csv", "a") as file:
            file.write(data + "\n")

def get_driver():
    opts = Options()
    opts.add_argument("user-agent=AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36")
    # opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36")
    opts.add_argument("--incognito")
    capabilities = webdriver.DesiredCapabilities.CHROME

    # PROXY = "189.89.168.132:4145"
    # prox = Proxy()
    # prox.proxy_type = ProxyType.MANUAL
    # prox.autodetect = False
    # prox.http_proxy = PROXY
    # prox.ssl_proxy = PROXY
    # prox.add_to_capabilities(capabilities)

    return webdriver.Chrome("./chromedriver", chrome_options=opts, desired_capabilities=capabilities)

def main():
    get_all_niche_details_data()

if __name__=="__main__":
    main()