# Programming Legend Group Project --- Data 21/Dec/2023

# libraries
import csv
import os
import time
from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient
import threading
# KivyMD - GUI
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock, mainthread

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
            pos_hint: {"center_y":0.92,"center_x":0.5}
            size_hint: 0.25, 0.25
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
            id: startButton
            text: "Start Process"
            size_hint: 0.66, 0.065
            pos_hint: {"center_y":0.20, "center_x":0.5}
            background_color: 0,0,0,0
            font_name: "Roboto"
            on_press: root.controller(ScrapNum, Skill, Location, self)
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

        MDFloatLayout:
            id: progress_layout
            md_bg_color: 1, 1, 1, 1
            Image:
                source: "assets/ZipRecruiterLogo.webp"
                pos_hint: {"center_y": 0.92, "center_x": 0.5}
                size_hint: 0.25, 0.25
            MDLabel:
                text: "Loading..."
                font_name: "Roboto-Bold"
                font_size: "25sp"
                size_hint_x: .90
                pos_hint: {"center_y": 0.73, "center_x": 0.5}
                halign: "center"
                color: rgba(4, 59, 92, 255)
            MDProgressBar:
                id: progress_bar
                value: 0
                size_hint: (0.8, None)
                height: dp(20)
                pos_hint: {"center_y": 0.5, "center_x": 0.5}


<OutputScreen>:
    MDFloatLayout:
        md_bg_color: 1,1,1,1
        Image:
            source: "assets/ZipRecruiterLogo.webp"
            pos_hint: {"center_y":0.92,"center_x":0.5}
            size_hint: 0.25, 0.25
        MDLabel:
            id: output
            text:"File Saved!!!"
            font_name: "Roboto-Bold"
            font_size: "25sp"
            size_hint_x: .90
            pos_hint: {"center_y":0.73,"center_x":0.5}
            halign: "center"
            color: rgba(4, 59, 92, 255)
        MDLabel:
            id: output
            text:"Press button to start process again"
            font_name: "Roboto-Bold"
            font_size: "14sp"
            size_hint_x: .90
            pos_hint: {"center_y":0.40,"center_x":0.5}
            halign: "center"
            color: rgba(4, 59, 92, 255)
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


# This Class is a Screen
# It is used to get jobs from the screen as well as trying to not make the screen freeze
# by using threading - where we can make use of scheduling to prevent to many jobs at once which is
# why the screen freezes, at last it didn't work as expected by it at least doesn't freeze the screen
# for as long as it did before.
class GetInformation(Screen):
    # this stop variable is used to stop the threading
    stop = threading.Event()

    # this is the first function that will happen when the user get to this screen (GetInformation)
    def on_enter(self, *args):
        # changes the GUI - specifically the progress bar and value
        self.ids.progress_layout.opacity = 0
        self.ids.progress_bar.value = 0

    # this functions sole purpose was to start the animation of loading so that the user knows that we are waiting
    # for the process of scrapping the jobs from the web is completed
    def start_ani(self, button_instance):
        # changes the GUI of this Screen so that we can see the progress bar and the value
        self.ids.progress_layout.opacity = 1
        self.ids.progress_bar.value = 0
        # here we are making use of CLock to schedule the update_progress into the queue where it will then be
        # processed into action
        Clock.schedule_interval(self.update_progress, 0.1)

    # this is the function that was just called before by the clock
    def update_progress(self, dt):
        # this is a simple while loop, while the progress value is <100
        if self.ids.progress_bar.value >= 100:
            self.ids.progress_bar.value = 0
        else:
            self.ids.progress_bar.value += 5

    # this will stop the animation, ani is short for animation.
    def stop_ani(self, button_instance):
        self.ids.progress_layout.opacity = 0

    # This is the Controller as I called it, since as it's name suggusts it controls the whole Screen.
    # when the button in the GUI is pressed it will activate this function which will then active each one of these
    # function is this class.
    def controller(self, ScrapNum, Skill, Location, button_instance):
        # three parameter from the GUI text input from user
        # activates the animation function
        Clock.schedule_once(self.start_ani, 0)
        # at almost the same time activates the do_it function
        threading.Thread(target=self.do_it, args=(ScrapNum, Skill, Location)).start()
        # stops the animation
        Clock.schedule_once(self.stop_ani, 0)
        #time.sleep(3)
        # goes to next screen using the next_screen function
        Clock.schedule_once(self.next_screen, 0)

    # this is the scrape which as the name mentions it will scrape jobs from where?
    # from the website
    def scrape(self, url, client):
        # Function to scrape job post websites and extract relevant information
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
                    # by using the xpath of certain div we can acces the data of that div
                    # which would then return the data we need
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

                            link_tag = job_info_container.find('h2', {'class': 'font-bold text-black text-header-sm'})
                            if link_tag is not None:
                                job_info['Links'] = link_tag.find('a')['href']

                            salary_container = job_info_container.find('div', {'class': 'flex flex-col gap-4'})
                            if salary_container is not None:
                                salary_tag = salary_container.find('div', {'class': 'mr-8'})
                                if salary_tag is not None:
                                    job_info['Salary'] = salary_tag.text
                                else:
                                    job_info['Salary'] = 'Not Specified'

                            job_listings.append(job_info)

            else:
                # will print out couldn't connect to the url that was made using user input
                print(f"Could not connect to {url}")

            time.sleep(1)

        except Exception as e:
            print("Connection failed. Please check your connection and try again.\n")
            print(e)

        return job_listings

    # functino do it well this one is the function to fist create the url with the user input then scrape
    # the data of the url that was just made, we give that url to scrape function that we already mentioned above
    # it at the end with the scrapes return of the jobs, will then be saved to
    def do_it(self, ScrapNum, Skill, Location, *args):
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
        # this is the base of the url where variables will be added to this to complete the full url
        base_url = 'https://www.ziprecruiter.com/jobs-search?'
        skill = userskill.strip()
        place = userplace.strip()
        place = place.split(',')
        place = place[0].title() + place[1].upper()

        # Use this api so that we are not block by the website, as berfore i was always block by the website
        client = ScrapingBeeClient(
            api_key='EKUKIQVHGO68Z4ZKCBINE7OTM447ZTG80ERJ0D5ROYIPGX65KP3GFQU2UU8T2WTZVX0M62B56C6QMWS3')

        # Craft the full URL with parameters
        results = []  # data

        data = results

        filename = f'Output/job_listings_{skill}.csv'
        # goes thourgh each website to find the data of each page that user has given
        for page in range(no_of_pages):
            full_url = f'{base_url}search={skill}&l={place}&page={page}'
            results.extend(self.scrape(full_url, client))

        file_exists = os.path.exists(filename)

        # here finally once data has been given we open the filename which is a varibale above and we add the data
        # from the scrape into the fields shown below
        with open(filename, 'a', newline='') as csv_file:

            fields = ['Title', 'CompanyName', 'Location', 'Links', 'Salary']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fields)

            if not file_exists:
                csv_writer.writeheader()
            # adds scrapped data to table
            csv_writer.writerows(data)

        # Prompt user with the path of the saved file
        print(f"Job listings saved as {filename}")

    # this @mainthread will be used so the threading in control will know to go to this go fast
    @mainthread
    # function next_screen will go to the next screen which is the output screen what will show that process is complete
    def next_screen(self, *args):
        MDApp.get_running_app().root.current = "outputscreen"


class OutputScreen(Screen):
    pass


# the start of Program class
class ReadME(MDApp):
    def build(self):
        # this will load the GUI part of the code named KV at the beginning
        GUI = Builder.load_string(KV)
        return GUI


# run the Class ReadME
ReadME().run()

# Finished