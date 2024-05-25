import csv
import os
import time
from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient


def scrape(url, client):
    """Function to scrape job post websites and extract relevant information"""
    job_listings = []

    try:
        # Get html response using ScrapingBee api
        response = client.get(url)

        # Check for connection success
        if response.status_code == 200:
            # Parse content of response as xml using BeautifulSoup
            soup = BeautifulSoup(response.content, 'lxml')

            # Get the most outermost html element that contains all information needed
            omega_tag = soup.find('div', {'class': 'mb-72 flex flex-col gap-24 md:gap-36 md:w-[460px]',
                                          'data-testid': 'job-results-root'})

            # To-dos
            # Identify HTML elements containing
            # 1. Job Title
            # 2. Company name
            # 3. Location
            # 4. Link
            # 5. Salary

            if omega_tag is not None:
                for i in omega_tag.find_all('div', {'class': 'flex flex-col gap-24 md:gap-36'}):
                    job_info = {}
                    job_info_container = i.find('article', {'class': 'group flex w-full flex-col text-black'})

                    if job_info_container is not None:
                        job_title_header = job_info_container.find('h2',
                                                                   {'class': 'font-bold text-black text-header-sm'})
                        if job_title_header is not None:
                            job_info['title'] = job_title_header.text

                        companyName_location_container = job_info_container.find('div', {
                            'class': 'mt-[4px] flex flex-col gap-4'})
                        location_tag = companyName_location_container.find('p', {
                            'class': 'text-black normal-case text-body-md'})
                        if location_tag is not None:
                            job_info['location'] = location_tag.text

                        company_name_tag = companyName_location_container.find('p', {
                            'class': 'text-black normal-case line-clamp-1 text-body-md'})
                        if company_name_tag is not None:
                            job_info['companyName'] = company_name_tag.text

                        link_tag = job_info_container.find('h2', {'class': 'font-bold text-black text-header-sm'})
                        if link_tag is not None:
                            job_info['links'] = link_tag.find('a')['href']

                        salary_container = job_info_container.find('div', {'class': 'flex flex-col gap-4'})
                        if salary_container is not None:
                            salary_tag = salary_container.find('div', {'class': 'mr-8'})
                            if salary_tag is not None:
                                job_info['salary'] = salary_tag.text
                            else:
                                job_info['salary'] = 'Not Specified'

                        job_listings.append(job_info)

        else:
            print(f"Could not connect to {url}")

        time.sleep(1)

    except Exception as e:
        print("Connection failed. Please check your connection and try again.\n")
        print(e)

    return job_listings


def save_to_csv(filename, data):
    """Function to save results to a csv file"""
    # Check if file exists, if it does, open it for appending, else open it for writing
    file_exists = os.path.exists(filename)

    with open(filename, 'a', newline='') as csv_file:
        fields = ['title', 'companyName', 'location', 'links', 'salary']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)

        if not file_exists:
            csv_writer.writeheader()

        csv_writer.writerows(data)

    # Prompt user with the path of the saved file
    print(f"Job listings saved to {filename}")


# Looping through the number of pages
def loop_through_pages():
    within_range = False
    while not within_range:
        no_of_pages = int(input('Enter the # of pages to scrape (max 10): '))
        if 1 <= no_of_pages <= 10:
            within_range = True

    base_url = 'https://www.ziprecruiter.com/jobs-search?'
    skill = input('Enter your Skill: ').strip()
    place = input('Enter the location: ').strip()
    place = place.split(',')
    place = place[0].title() + place[1].upper()
    client = ScrapingBeeClient(
        api_key='U8GXCXCV1L0GY592D1HLK0594W1WTB3XG4C4851BHBMJII14P10W0VA678GCMMG52ZL6XIN9M5J2SN1H')

    # Craft the full URL with parameters
    results = []
    for page in range(no_of_pages):
        full_url = f'{base_url}search={skill}&l={place}&page={page}'
        results.extend(scrape(full_url, client))

    return results


csv_file = '../job_listings.csv'

# Call save_to_csv function to save results to a csv file
save_to_csv(csv_file, loop_through_pages())
