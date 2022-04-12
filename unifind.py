#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from playsound import playsound
import threading
import webbrowser
import json


class Unifind:
    def __init__(self):
        self.options = Options()
        # This prevents getting spammed with endless geckodriver tabs.
        self.options.headless = True
        self.alarm_sound = "product_alarm.wav"
        self.options_file = "options.json"
        self.product_list_file = "product_list.txt"
        self.product_list = None
        self.update_interval = 15
        self.opened_urls = []
        self.browser = webdriver.Firefox(options=self.options)
        self.json_blob = None


    # The main entry point of the application.
    def check_product_urls(self):
        threading.Timer(self.update_interval, self.check_product_urls).start()
        # So this function repeats itself every X seconds.
        try:
            # Reload, in case the user edited the file.
            self.load_json()

        # Kill the schedule if the program is murderlized.
        except (KeyboardInterrupt, SystemExit):
            self.browser.close()


    #  This functions checks pages to see if any products are in stock.
    def check_page(self, **kwargs):
        url = kwargs.get("url")
        self.browser.get(url)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        title = soup.findAll("h1", {"class":"comProduct__title"})[0].text

        # Check if the product is available given our search conditions.
        if self.is_product_available(soup, **kwargs):
            self.open_browser_to_site(url, title)

    # Boolean function used by self.check_page to see if the product is available.
    @staticmethod
    def is_product_available(soup, **kwargs):
        try:
            if kwargs.get("query") in soup.findAll(kwargs.get("element"), {kwargs.get("key"): kwargs.get("value")})[0].text:
                return True
        except IndexError:
            pass
        return False

    # This function opens a browser if available.
    def open_browser_to_site(self, url, title):
        if url not in self.opened_urls:
            self.opened_urls.append(url)
            print(f"[!] Product {title} is available @ {url}. Opening window.")
            self.play_alarm()
            webbrowser.get("chrome").open_new_tab(url)

    # This function plays a sound before opening the browser.
    def play_alarm(self):
        playsound(self.alarm_sound)


    # Load json from the options file.
    def load_json(self):
        with open(self.options_file, "r") as f:
            self.json_blob = json.loads(f.read())

        for item in self.json_blob:
            self.parse_json_element(item)


    # Get the json response from each item.
    def parse_json_element(self, item):
        self.check_page(url=item.get("url"), element=item.get("element"), key=item.get("key"),
                        value=item.get("value"), query=item.get("query"))


if __name__ == "__main__":
    try:
        u = Unifind()
        u.check_product_urls()
    except ConnectionRefusedError:
        pass
    except ConnectionAbortedError:
        pass
    except ConnectionResetError:
        pass
    except TimeoutError:
        pass
    except TimeoutException:
        pass
