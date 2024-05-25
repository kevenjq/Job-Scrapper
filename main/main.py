# Programming Legend Group Project --- Data 21/Dec/2023


"""

Objective: Job Posting Scraper -
           Develop a web scraper that extracts job postings from a popular job board website.

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

div = soup.find_all('div', jsname_="CaV2mb", class_="zxU94d gws-plugins-horizon-jobs__tl-lvc")

print(soup)




def get_url(job_title):
    template = "https://de.indeed.com/jobs?q={}&l=Berlin&vjk=bb3e22f398ee21a6"
    url = template.format(job_title)
    return url


url = get_url("engineer")
print(url)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

cookie = {
    "Cookie" : 'NID=511=QOzx55ymGM8bIWtyFFi4QcxaKUs6ooD_nY9uioAxuWhCOeEMeHdB-IeXGQD8B2mnCUSem9UhUbJDu3oOAGd3PZ3LpX9H1AqYRnIeBJ5osUxViA6t8MeR4LOGud09Dvs5igwyyrBZ2xjXqR4_iC0voCF4KCuffOEMG8lyQvPFhScngbyFaeoMr2cop0IE1fMs6CZbv3H3feNCSM3deqR2E19KXao'
}

response = requests.get(url, headers)
time.sleep(5)

soup = BeautifulSoup(response.text, 'lxml')

parent = soup.find('div', class_="search-job-list-body")

cards = soup.find_all("div",class_="jobsearch-jobcard-wrapper")


print(response.text)
print(response.reason)
print(cards)


"""
# ^ stuff that I have tried to use


import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def get_current_url(url, job_title, location):

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.XPATH,'//*[@id="text-input-what"]').send_keys(job_title)
    time.sleep(3)
    driver.find_element(By.XPATH,'//*[@id="text-input-where"]').send_keys(location)
    time.sleep(3)
    driver.find_element(By.XPATH,'/html/body/div').click()
    time.sleep(3)
    try:
        driver.find_element(By.XPATH,'//*[@id="jobsearch"]/div/div[2]/button').click()
    except:
        driver.find_element(By.XPATH,'//*[@id="whatWhereFormId"]/div[3]/button').click()
    current_url = driver.current_url

    return current_url


def scrape_job_details(url):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=HEADERS)
    content = BeautifulSoup(resp.content, 'lxml')

    jobs_list = []
    for post in content.select('.job_seen_beacon'):
        try:
            data = {
                "job_title": post.select('.jobTitle')[0].get_text().strip(),
                "company": post.select('.companyName')[0].get_text().strip(),
                "rating": post.select('.ratingNumber')[0].get_text().strip(),
                "location": post.select('.companyLocation')[0].get_text().strip(),
                "date": post.select('.date')[0].get_text().strip(),
                "job_desc": post.select('.job-snippet')[0].get_text().strip()

            }
        except IndexError:
            continue
        jobs_list.append(data)
    dataframe = pd.DataFrame(jobs_list)

    return dataframe


current_url = get_current_url('https://de.indeed.com/','Data Scientist',"Berlin")

df = scrape_job_details(current_url)

df.to_csv("jobs.csv")

