#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from playsound import playsound
import webbrowser
import requests
import json
import sys
import threading


class Unifind:
    def __init__(self):
        self.options = Options()
        # This prevents getting spammed with endless geckodriver tabs.
        self.options.headless = True
        self.alarm_sound = "product_alarm.wav"
        self.product_list_file = "product_list.txt"
        self.product_list = None
        self.update_interval = 10.0
        self.opened_urls = []
        self.browser = webdriver.Firefox(options=self.options)


    # Load the product_list.txt file and assign it to self.product_list.
    def load_product_urls(self):
        with open(self.product_list_file, "r") as f:
            self.product_list = f.read().splitlines()


    # The main entry point of the application.
    def check_product_urls(self):
        # So this function repeats itself every X seconds.
        threading.Timer(self.update_interval, self.check_product_urls).start()

        # Reload, in case the user edited the file.
        self.load_product_urls()

        for product_url in self.product_list:
            self.check_page(product_url)

    #  This functions checks pages to see if any products are in stock.
    def check_page(self, url):
        page = self.browser.get(url)
        try:
            soup = BeautifulSoup(page.page_source)
            # Close the browser so we don't exhaust computer resources.
            page.close()

            if self.is_product_available(soup):
                print("[!] Product is available. Opening window.")
                self.open_browser_to_site(url)
        except AttributeError:
            pass

    # Boolean function used by self.check_page to see if the product is available.
    @staticmethod
    def is_product_available(soup):
        # Single product pages with single packs have a different set of (default) options.
        if not soup.findAll("span", {"class": "relatedProducts__item__data__price"})[0].text == "Sold Out":
            return True

        # The camera page has a different set of options.
        if not soup.findAll("span", {"class": "comProduct__badge"})[0].text == "Sold Out":
            return True

        # Third product page, such as video receivers.
        if soup.findAll("button", {"class": "btn btn--full"})[0].text == "Sold Out":
            return True

        return False


    # This function opens a browser if available.
    def open_browser_to_site(self, url):
        self.play_alarm()
        if url not in self.opened_urls:
            webbrowser.get('firefox').open_new_tab(url)
            self.opened_urls.append(url)

    # This function plays a sound before opening the browser.
    def play_alarm(self):
        playsound(self.alarm_sound)


if __name__ == "__main__":
    u = Unifind()
    u.check_product_urls()
