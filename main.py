from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

PATH = '/home/kali/Downloads/geckodriver'
driver = webdriver.Firefox(executable_path=PATH)
url = "https://teams.microsoft.com/"
with open('creds.txt', 'r') as creds:
    creds = creds.read().split()
    email = creds[0]
    pas = creds[1]

driver.get(url)
time.sleep(3)
driver.find_element_by_name('loginfmt').send_keys(email)
time.sleep(2)
driver.find_element_by_id('idSIButton9').click()
time.sleep(2)
driver.find_element_by_name('passwd').send_keys(pas)
time.sleep(2)
driver.find_element_by_id('idSIButton9').click()
time.sleep(2)
driver.find_element_by_id('idBtn_Back').click()
time.sleep(2)
driver.find_element_by_class_name('use-app-lnk').click()
time.sleep(5)
driver.find_element_by_xpath("//*[contains(text(),'Azad')]").click()
n = 3

try:
    driver.find_element_by_class_name(
        'ts-sym ts-btn ts-btn-primary inset-border icons-call-jump-in ts-calling-join-button app-title-bar-button app-icons-fill-hover call-jump-ink').click()
except:
    print('No join link')
