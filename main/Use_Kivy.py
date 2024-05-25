# Programmer: Keven Quevedo-----Date Finished: 26/Apr/2023
# This program is about a Face Recognition that will find your Face.
# It also includes a Login System plus a Background Remover using Removebg api.


# libraries
import csv
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient
import dfgui
import threading
# KivyMD
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

# The Window size for every window
Window.size = (600, 700)

# The GUI, using KivyMD
KV = """
# Here you can see the different pages in the application
ScreenManager:
    DefaultMain:
        name: "defaultmain"
    GetInformation:
        name: "getinformation"
    OutputScreen:
        name: "outputscreen"

<DefaultMain>:
    MDFloatLayout:
        md_bg_color: 1,1,1,1
        Image:
            source: "assets/ZipRecruiterLogo.webp"
            pos_hint: {"center_y":0.82,"center_x":0.5}
            size_hint: 0.5, 0.5
        MDLabel:
            text:"Programming LEGENDS"
            font_name: "Roboto-Bold"
            font_size: "25sp"
            size_hint_x: .90
            pos_hint: {"center_y":0.73,"center_x":0.5}
            halign: "center"
            color: rgba(4, 59, 92, 255)
        MDLabel:
            text:"By: Keven, Ritik, Emmanuel"
            font_name: "Roboto-Bold"
            font_size: "15sp"
            size_hint_x: .55
            pos_hint: {"center_y":0.65,"center_x":0.5}
            halign: "center"
            color: rgba(4, 59, 92, 255)
        MDLabel:
            text:"Press 'Start' to find jobs in your field"
            font_name: "Roboto-Bold"
            font_size: "15sp"
            size_hint_x: .55
            pos_hint: {"center_y":0.25,"center_x":0.5}
            halign: "center"
            color: rgba(4, 59, 92, 255)
        Button:
            text: "Start Process"
            size_hint: 0.66,0.065
            pos_hint: {"center_x":0.5,"center_y":0.18}
            background_color: 0,0,0,0
            font_name: "Roboto"
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "getinformation"
            canvas.before:
                Color:
                    rgb: rgba(50, 138, 255, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [5]
        Button:
            text: "Exit App"
            size_hint: 0.66,0.065
            pos_hint: {"center_x":0.5,"center_y":0.09}
            background_color: 0,0,0,0
            font_name: "Roboto"
            color: rgba(3, 138, 255, 255)
            on_release: app.stop()
            canvas.before:
                Color:
                    rgb: rgba(50, 138, 255, 255)
                Line:
                    width: 1.2
                    rounded_rectangle: self.x, self.y, self.width, self.height, 5,5,5,5, 100
                    
<GetInformation>:
    MDFloatLayout:
        md_bg_color: 1,1,1,1
        Image:
            source: "assets/ZipRecruiterLogo.webp"
            pos_hint: {"center_y":0.82,"center_x":0.5}
            size_hint: 0.35, 0.35
        MDLabel:
            text:"Get Job Posts"
            font_name: "Roboto-Bold"
            font_size: "25sp"
            size_hint_x: .90
            pos_hint: {"center_y":0.73,"center_x":0.5}
            halign: "center"
            color: rgba(4, 59, 92, 255) 
        MDTextField:
            id: ScrapNum
            input_filter: "int"
            write_tab: False
            pos_hint: {"center_y": 0.50, "center_x": 0.5}
            size_hint: (0.55,0.1)
            hint_text : 'Pages to Scrape from(max 10)'
            helper_text: 'Example: 1'
        MDTextField:
            id: Skill
            write_tab: False
            pos_hint: {"center_y": 0.40, "center_x": 0.5}
            size_hint: (0.55,0.1)
            hint_text : 'Your Job'
            helper_text: 'Data Scientist'
        MDTextField:
            id: Location
            write_tab: False
            pos_hint: {"center_y": 0.30, "center_x": 0.5}
            size_hint: (0.55,0.1)
            hint_text : 'Location'
            helper_text: 'Berlin, Germany'
            
        Button:
            text: "Start Process"
            size_hint: 0.66,0.065
            pos_hint: {"center_y":0.20,"center_x":0.5}
            background_color: 0,0,0,0
            font_name: "Roboto"
            on_press: root.do_it(ScrapNum, Skill, Location)
            canvas.before:
                Color:
                    rgb: rgba(50, 138, 255, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [5]
            on_release:
                root.manager.transition.direction = "up"
                root.manager.current = "outputscreen"
                
<OutputScreen>:
    MDFloatLayout:
        md_bg_color: 1,1,1,1
        Image:
            source: "assets/ZipRecruiterLogo.webp"
            pos_hint: {"center_y":0.92,"center_x":0.5}
            size_hint: 0.25, 0.25
        MDLabel:
            text:"Finished Process"
            font_name: "Roboto-Bold"
            font_size: "25sp"
            size_hint_x: .90
            pos_hint: {"center_y":0.73,"center_x":0.5}
            halign: "center"
            color: rgba(4, 59, 92, 255)
        MDLabel:
            text:"File Saved Successfully"
            font_name: "Roboto-Bold"
            font_size: "25sp"
            size_hint_x: .90
            pos_hint: {"center_y":0.65,"center_x":0.5}
            halign: "center"
            color: rgba(3, 138, 255,1)

        Button:
            text: "Start Process Again"
            size_hint: 0.66,0.065
            pos_hint: {"center_y":0.30,"center_x":0.5}
            background_color: 0,0,0,0
            font_name: "Roboto"
            on_press:
                root.manager.transition.direction = "left"
                root.manager.current = "getinformation"
            canvas.before:
                Color:
                    rgb: rgba(50, 138, 255, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [5]
"""


# Start of all classes
# First window when program starts
class DefaultMain(Screen):
    pass


# Gets the Information from user Screen
class GetInformation(Screen):

    def scrape(self, url, client):
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
                                job_info['Title'] = job_title_header.text

                            companyName_location_container = job_info_container.find('div', {
                                'class': 'mt-[4px] flex flex-col gap-4'})
                            location_tag = companyName_location_container.find('p', {
                                'class': 'text-black normal-case text-body-md'})
                            if location_tag is not None:
                                job_info['Location'] = location_tag.text

                            company_name_tag = companyName_location_container.find('p', {
                                'class': 'text-black normal-case line-clamp-1 text-body-md'})
                            if company_name_tag is not None:
                                job_info['CompanyName'] = company_name_tag.text

                            # link_tag = job_info_container.find('h2', {'class': 'font-bold text-black text-header-sm'})
                            # if link_tag is not None:
                            # job_info['Links'] = link_tag.find('a')['href']

                            salary_container = job_info_container.find('div', {'class': 'flex flex-col gap-4'})
                            if salary_container is not None:
                                salary_tag = salary_container.find('div', {'class': 'mr-8'})
                                if salary_tag is not None:
                                    job_info['Salary'] = salary_tag.text
                                else:
                                    job_info['Salary'] = 'Not Specified'

                            job_listings.append(job_info)

            else:
                print(f"Could not connect to {url}")

            time.sleep(1)

        except Exception as e:
            print("Connection failed. Please check your connection and try again.\n")
            print(e)

        return job_listings

    def do_it(self, ScrapNum, Skill, Location):
        global no_of_pages
        userskill = Skill.text
        userplace = Location.text
        userpages = ScrapNum.text

        within_range = False
        while not within_range:
            # I need to add verification that it is a num
            no_of_pages = int(userpages)
            if 1 <= no_of_pages <= 10:
                within_range = True

        base_url = 'https://www.ziprecruiter.com/jobs-search?'
        skill = userskill.strip()
        place = userplace.strip()
        place = place.split(',')
        place = place[0].title() + place[1].upper()
        client = ScrapingBeeClient(
            api_key='61C8FV3CNHIG3N20SLBWGBWLRXSMRR4OPXYEJ27OS6F0EXGT95W0Y5D25NW37P482KBB1SEVJ5SUZOKD')

        # Craft the full URL with parameters
        results = []  # data

        data = results

        filename = f'Output/job_listings_{skill}.csv'

        for page in range(no_of_pages):
            full_url = f'{base_url}search={skill}&l={place}&page={page}'
            results.extend(self.scrape(full_url, client))

        file_exists = os.path.exists(filename)

        with open(filename, 'a', newline='') as csv_file:
            #  'links',
            fields = ['Title', 'CompanyName', 'Location', 'Salary']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fields)

            if not file_exists:
                csv_writer.writeheader()
            # adds scrapped data to table
            csv_writer.writerows(data)

        # Prompt user with the path of the saved file
        print(f"Job listings saved as {filename}")


# Saves job csv file
class OutputScreen(Screen):
    def close_username_dialogue(self, obj):
        self.dialog.dismiss()

    # not using
    def ShowOutput(self):
        try:
            dataframe = pd.read_csv('../job_listings.csv')
            dataframe.to_string()
            dfgui.show(dataframe)
        except:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
            dialog = MDDialog(
                title="Somethings didn't work",
                text="Please try again later",
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue])
            dialog.open()

    # not using
    def displayCard(self):
        cancel_btn_username_dialogue = MDFlatButton(text='Close', on_release=self.close_username_dialogue)
        dialog = MDDialog(
            title="File Saved",
            text="Successfully Saved File",
            size_hint=(0.7, 0.2),
            buttons=[cancel_btn_username_dialogue])
        dialog.open()


# the start of Program class
class ReadME(MDApp):
    def build(self):
        # this will load the GUI part of the code named KV at the beginning
        GUI = Builder.load_string(KV)
        return GUI


# run the Class ReadME
ReadME().run()

"""
    def on_stop(self):
        # open a file
        f = open("whoisloginedin.txt", "a")
        f.seek(0)
        # delete all contents in file
        f.truncate()
        f = open("path_image","a")
        f.seek(0)
        f.truncate()
        # turn of camera
        Camera(play=False)
"""
