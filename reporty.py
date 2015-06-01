#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import click

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
def wait_until_element_available(driver, timeout, selectortype, selector):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((selectortype, selector))
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
    wait_until_element_available(driver, 10, By.ID, 'chkLDAPTunnistus')
    driver.find_element_by_id('chkLDAPTunnistus').click()
    driver.find_element_by_id('itxtUserID').send_keys(username)
    driver.find_element_by_id('itxtPassword').send_keys(password)
    driver.find_element_by_id('icmdOk').click()

    errorMsg = check_if_element_available(driver, 'SBErrorText')
    if errorMsg is not None:
        print "Login failed... " + errorMsg.text
        exit(1)

def go_to_worktimes(driver):
    driver.find_element_by_class_name('uiMenuWork').click()
    wait_until_element_available(driver, 10, By.ID, 'prlWTEP_uwtWorkTime__ctl0_rlbLisaaTyoaika')
    driver.find_element_by_id('prlWTEP_uwtWorkTime__ctl0_rlbLisaaTyoaika').click()

def get_worktime_cells(driver, projectname, date=None):
    selector = ".WTGCellWrapper input[title*='{projectname}']".format(projectname=projectname)
    if date is not None:
        selector += "[title*='{date}']".format(date=date)
    return driver.find_elements_by_css_selector(selector)

def input_worktime(driver, element, duration, description):
    element.click()
    wait_until_element_available(driver, 10, By.NAME, 'prlWTEP$uwtWorkTime$_ctl1$ctlMnth$ctlWorkTimeTaskAtlasEditForm1$txtHours')
    driver.find_element_by_name('prlWTEP$uwtWorkTime$_ctl1$ctlMnth$ctlWorkTimeTaskAtlasEditForm1$txtHours').send_keys(duration)
    wait_until_element_available(driver, 10, By.NAME, 'prlWTEP$uwtWorkTime$_ctl1$ctlMnth$ctlWorkTimeTaskAtlasEditForm1$txtDescription')
    sleep(0.2)
    driver.find_element_by_name('prlWTEP$uwtWorkTime$_ctl1$ctlMnth$ctlWorkTimeTaskAtlasEditForm1$txtDescription').send_keys(description)
    driver.execute_script("__doPostBack('prlWTEP$uwtWorkTime$_ctl1$ctlMnth$ctlWorkTimeTaskAtlasEditForm1$rlbSave','') ")

@click.command()
@click.option('--date', default=time.strftime("%d.%m.%Y"), help='Work date. Default is today')
@click.option('--desc', default=None, help='Work description.')
@click.option('--hours', default=None, help='Working hours.', type=click.FLOAT)
def main(date, desc, hours):
    """Command line tool for interacting with Reportronic"""

    settings = load_settings_from_json()
    driver = init_driver()

    driver.get(settings['url'])
    login_to_reportronic(settings['username'], settings['password'], driver)
    go_to_worktimes(driver)
    wait_until_element_available(driver, 10, By.CLASS_NAME, 'WTGCellWrapper')

    test = get_worktime_cells(driver, 'JAMK', date=date)
    input_worktime(driver, test[0], hours, desc)

if __name__ == '__main__':
    main()