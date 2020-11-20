from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import date, datetime
from schedule import classes


def get_day():
    return datetime.now().weekday()


def get_time():
    return datetime.now().time()


opt = webdriver.ChromeOptions()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")

# opt.add_argument("--start-maximized")
# Pass the argument 1 to allow and 2 to block permissions
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
},)
opt.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=opt)

url = "https://teams.microsoft.com/"
with open('creds.txt', 'r') as creds:
    creds = creds.read().split()
    email = creds[0]
    pas = creds[1]


def login():
    global driver
    # enter email and click on login
    driver.find_element(By.NAME, 'loginfmt').send_keys(email)
    time.sleep(5)
    driver.find_element(By.ID, 'idSIButton9').click()
    time.sleep(5)

    # enter password and click on login
    driver.find_element(By.NAME, 'passwd').send_keys(pas)
    time.sleep(5)
    driver.find_element(By.ID, 'idSIButton9').click()
    time.sleep(5)

    # clicks on button where it asks to remeber the user
    # clicks on no to have the consistency in each instance of login
    driver.find_element(By.ID, 'idBtn_Back').click()
    time.sleep(5)

    # proceeds onto website when asked to continue on app
    driver.find_element(By.CLASS_NAME, 'use-app-lnk').click()


def join(clas):
    global driver

    time.sleep(5)
    driver.find_element(By.XPATH, f"//*[contains(text(),'{clas}')]").click()
    time.sleep(5)
    try:
        driver.find_element(
            By.XPATH, '//*[@title="Join call with video"]').click()
    except:
        print('No join link')

    time.sleep(10)

    camera = driver.find_element(
        By.XPATH, '//toggle-button[@text = "Enable video"]')
    if camera.get_attribute('title') == 'Turn camera off':
        camera.click()
    time.sleep(5)

    microphone = driver.find_element(By.ID, 'preJoinAudioButton')
    if microphone.get_attribute('title') == 'Mute microphone':
        microphone.click()
    time.sleep(5)

    driver.find_element(
        By.XPATH, '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button').click()
    time.sleep(3600)
    leave_class()


def leave_class():
    global driver


def main():
    global driver
    driver.get(url)
    time.sleep(5)

    if 'login' in driver.current_url:
        login()
    day = get_day()
    clas = classes(day)
    for c in clas:
        print(c[0])
        join(c[0])


main()
