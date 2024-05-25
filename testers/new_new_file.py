from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.metrics import dp
import pandas as pd

from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.datatables import MDDataTable
import csv
import csv
import os
import time
from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient
import dfgui
# KivyMD
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

"""
    def __init__(self, **kwargs):
        super(CSVDisplay, self).__init__(**kwargs)

        # Read the CSV file
        with open('job_listings.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Create GridLayout to hold labels
            layout = GridLayout(cols=3, spacing=50, size_hint_y=None)
            layout.bind(minimum_height=layout.setter('height'))

            # Create labels for column headers
            headers = reader.fieldnames
            for header in headers:
                header_label = Label(text=header)
                layout.add_widget(header_label)

            # Iterate through each row in the CSV and display its content
            for row in reader:
                for col in headers:
                    row_label = Label(text=row[col], size_hint_y=None, height=40)
                    layout.add_widget(row_label)

            # Put the GridLayout inside a ScrollView
            scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
            scroll_view.add_widget(layout)
            self.add_widget(scroll_view)
"""

KV = """
ScreenManager:
    CSVDisplay:
        name : "csvdisplay"
        
<CSVDisplay>:
    MDFloatLayout:
        md_bg_color: 1,1,1,1
    Button:
        text: "show"
        on_press: root.ShowOutput()
"""

Window.size = (780, 680)


class CSVDisplay(Screen):
    def close_username_dialogue(self, obj):
        self.dialog.dismiss()
    # Not using
    def ShowOutput(self):
        try:
            filename = 'job_listings.csv'

            # Read the CSV file
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = [dict(row) for row in reader]

                # Ensure that the data is not empty
                if data:
                    # Create MDDataTable
                    table = MDDataTable(
                        column_data=[
                            ("Title", dp(30)),
                            ("Location", dp(30)),
                            ("Salary", dp(30))
                        ],
                        row_data=data,
                    )

                    # Show the MDDataTable
                    self.add_widget(table)
                else:
                    print("CSV data is empty.")

        except Exception as e:
            print(f"An error occurred: {e}")


class ReadME(MDApp):
    def build(self):
        # this will load the GUI part of the code named KV at the beginning
        GUI = Builder.load_string(KV)
        return GUI


if __name__ == '__main__':
    ReadME().run()
