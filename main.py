from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import date, datetime
from schedule import classes
from discord_notify import notify, notify_status
'''
PATH = '/home/kali/Downloads/geckodriver'
driver = webdriver.Firefox(executable_path=PATH)
'''
url = "https://teams.microsoft.com/"
with open('creds.txt', 'r') as creds:
    creds = creds.read().split()
    email = creds[0]
    pas = creds[1]
def get_driver():
    opt = webdriver.ChromeOptions()
    opt.add_argument("--disable-infobars")
    opt.add_argument("start-maximized")
    opt.add_argument("--disable-extensions")
    opt.add_argument("headless")
    # opt.add_argument("--start-maximized")
    # Pass the argument 1 to allow and 2 to block permissions
    opt.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1
    },)
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    return webdriver.Chrome(options=opt)



def get_day():
    return datetime.now().weekday()


def get_time():
    return datetime.now().time()


def login():
    global driver
    print("Logging in...")
    # enter email and click on login
    driver.find_element(By.NAME, 'loginfmt').send_keys(email)
    driver.find_element(By.ID, 'idSIButton9').click()
    time.sleep(3)

    # enter password and click on login
    driver.find_element(By.NAME, 'passwd').send_keys(pas)
    driver.find_element(By.ID, 'idSIButton9').click()
    time.sleep(3)

    # clicks on button where it asks to remeber the user
    # clicks on no to have the consistency in each instance of login
    driver.find_element(By.ID, 'KmsiCheckboxField').click()
    driver.find_element(By.ID, 'idSIButton9').click()
    time.sleep(10)
    #idBtn_Back
    # proceeds onto website when asked to continue on app
    driver.find_element(By.CLASS_NAME, 'use-app-lnk').click()


def join_button():
    global driver
    t = 15
    while t > 0:
        try:
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@title="Join call with video"]').click()
            return True
        except:
            print('Waiting for class to start....')
            t -= 1
            time.sleep(60)
            driver.refresh()
    return False

def join(sub):
    global driver

    #this code is for finding the team in list view
    #driver.find_element(By.XPATH,f'//*[@title="{sub}"]').click()

    #we find the team in grid view
    driver.find_element(By.XPATH, f"//*[contains(text(),'{sub}')]").click()
    time.sleep(3)

    if not join_button():
        txt = f"Could not join class for {sub} till {get_time()}."
        notify(txt, sub)
        print(txt)
        return False

    time.sleep(5)

    camera = driver.find_element(
        By.XPATH, '//toggle-button[@text = "Enable video"]')
    if camera.get_attribute('title') == 'Turn camera off':
        camera.click()
    time.sleep(1)

    microphone = driver.find_element(By.ID, 'preJoinAudioButton')
    if microphone.get_attribute('title') == 'Mute microphone':
        microphone.click()
    time.sleep(2)

    #joining class
    driver.find_element(
        By.XPATH, '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button').click()
    time.sleep(2)


    txt = f"Joined class for {sub}, on {get_time()}."
    print(txt)
    notify(txt, sub)
    return True


def leave_class(sub):
    global driver
    print("leaving class")
    #time_now = get_time()
    
    
    # end meeting
    time.sleep(3)
    try:
        driver.find_element_by_class_name("ts-calling-screen").click()
        driver.find_element_by_xpath('//*[@id="teams-app-bar"]/ul/li[3]').click() #come back to homepage
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="hangup-button"]').click()
        #driver.find_element(By.XPATH, '//*[@id="hangup-button"]').click()
        time.sleep(1)

        #go home
        driver.find_element(By.XPATH, '//*[@id="app-bar-2a84919f-59d8-4441-a975-2a8c2643b741"]').click()
    except:
        txt = f"Could not leave meeting for {sub} on {get_time()}."
        notify(txt, sub)
        return False
    # go to home page
    
    txt = f"Left meeting for {sub}, on {get_time()}"
    notify(txt, sub)
    return True


def main():
    global driver
    day = get_day()
    schedule_today = classes('test')
    schedule_today = [['Azad', 10, 11], ["Biomolecular NMR", 11, 12]]

    if not schedule_today:
        txt = 'No classes scheduled for today!'
        notify(txt)
        print(txt)
        return
    
    
    driver = get_driver()
    driver.get(url)
    time.sleep(5)

    if 'login' in driver.current_url:
        login()
        time.sleep(3)

    for event in schedule_today:
        sub = event[0]
        start_time, end_time = event[1], event[2]
        #duration in seconds
        duration = (end_time - start_time)*30
        print(sub)
        status = join(sub)
        #notify_status('Join',c[0], status)
        if not status:
            print('Goint to wait for 45 minutes.')
            time.sleep(45*60)
            continue
        else:
            time.sleep(duration)

        leave_class(sub)
        
    driver.quit()


main()
