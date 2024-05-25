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
    driver.find_element(By.XPATH, '//*[@id="text-input-what"]').send_keys(job_title)
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="text-input-where"]').send_keys(location)
    time.sleep(3)
    driver.find_element(By.XPATH, '/html/body/div').click()
    time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="jobsearch"]/div/div[2]/button').click()

    job_avali = True
    while job_avali:
        try:
            data = {
                "job_title": driver.find_element(By.XPATH,
                                                 '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div/div[1]/div/div/div/table[1]/tbody/tr/td/div[1]/h2'),
                "company": driver.find_element(By.XPATH,
                                               '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div/div[1]/div/div/div/table[1]/tbody/tr/td/div[2]/div/span[1]'),
                "location": driver.find_element(By.XPATH,
                                                '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div/div[1]/div/div/div/table[1]/tbody/tr/td/div[2]/div/div'),
                "job_desc": driver.find_element(By.XPATH,
                                                '//*[@id="mosaic-provider-jobcards"]/ul/li[1]/div/div[1]/div/div/div/table[2]/tbody/tr[2]/td/div/div/ul/li')
            }
        except IndexError:
            job_avali = False
            print("empty")
            continue

        return data["job_title"].text, data["company"].text, data["location"].text, data["job_desc"].text

    # Idea is to have a list of popular job posting websites and
    # gets it from a csv where user enters the company name and code finds the main url part


#jobWebsite = str(input("Enter Website name, e.g. Indeed\n:"))
#jobTitle = str(input("Enter Job title, eg. Data Scientist\n:"))
#jobLocation = str(input("Enter Location, e.g. Berlin\n:"))

#websiteIndex = {'company': [0, 1, 2, 3], 'job': pd.Series[2, 3], 'location': [0, 1, 2, 3]}

# websiteIndex = {
#    "Indeed" or "indeed": 'https://de.indeed.com/''',


# }


main_data = get_current_url("https://de.indeed.com/", "python", "berlin")

jobs_list = [main_data]

dataframe = pd.DataFrame(jobs_list)

#print(dataframe)

dataframe.to_csv("jobs.csv")
