#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
__author__ = 'matti'


# Initialize webdriver
def init_driver():
    driver = webdriver.Firefox()
    driver.set_window_size(1024, 768)
    return driver

# Load stuff from config.json
def load_settings_from_json():
    with open('config.json') as settings_file:
        settings = json.load(settings_file)
        return settings

# Waits set amount of time until element is visible
def wait_until_element_available(driver, id, timeout):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, id))
        )
    finally:
        return

# Checks if element exists, returns it if it does.
def check_if_element_available(driver, class_name):
    try:
        element = driver.find_element_by_class_name(class_name)
        return element
    except NoSuchElementException:
        return None

# Logs in to Reportronic...
def login_to_reportronic(username, password, driver):
    wait_until_element_available(driver, "chkLDAPTunnistus", 5)
    driver.find_element_by_id('chkLDAPTunnistus').click()
    driver.find_element_by_id('itxtUserID').send_keys(username)
    driver.find_element_by_id('itxtPassword').send_keys(password)
    driver.find_element_by_id('icmdOk').click()

    errorMsg = check_if_element_available(driver, 'SBErrorText')
    if errorMsg is not None:
        print "Login failed... " + errorMsg.text



# Load settings, create webdriver, login to reportronic...
def main():
    settings = load_settings_from_json()
    driver = init_driver()

    driver.get(settings['url'])
    login_to_reportronic(settings['username'], settings['password'], driver)

if __name__ == '__main__':
    main()