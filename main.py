from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import date, datetime
from schedule import classes
from discord_notify import notify
from creds import get_email, get_password
'''
PATH = '/home/kali/Downloads/geckodriver'
driver = webdriver.Firefox(executable_path=PATH)
'''

# if on windows set PATH = None and download chromedriver and add it to your windows PATH
PATH = '/home/arjun/Downloads/chromedriver'
url = "https://teams.microsoft.com/"


def main():
    global driver
    day = get_day()
    schedule_today = classes(day)
    #testcase
    schedule_today = [["Biomolecular NMR", 11, 12],['Azad', 10, 11]]

    if not schedule_today:
        txt = 'No classes scheduled for today!'
        # notify on discord
        notify(txt, "Any subject")
        print(txt)
        return
    
    #get web driver and open browser    
    driver = get_driver()
    driver.get(url)
    time.sleep(5)

    #if we need to login, invoke login
    if 'login' in driver.current_url:
        login()
        time.sleep(3)

    # now for every class we have in our schedule on current day we try to join the meeting
    for i in range(len(schedule_today)):
        event = schedule_today[i]
        sub = event[0]
        start_time, end_time = event[1], event[2]
        #duration in seconds
        duration = (end_time - start_time)*30
        print(sub)
        joined = join(sub)
        #notify_status('Join',c[0], status)
        if not joined:
            if i == len(schedule_today) - 1:
                print("No more classes today!")
                return
            # calculate waiting time for next class in our schedule
            wait_time = schedule_today[i+1][1] - start_time - 15
            print(f'Goint to wait for {wait_time} minutes.')
            time.sleep(wait_time*60)
            continue
        else:
            time.sleep(duration)

        leave_class(sub)
        
    driver.quit()


def get_discord_url():
    return discord_url


def get_driver():
    opt = webdriver.ChromeOptions()
    opt.add_argument("--disable-infobars")
    opt.add_argument("start-maximized")
    opt.add_argument("--disable-extensions")
    #this option uses headless browser
    ##opt.add_argument("headless")  

    # Pass the argument 1 to allow and 2 to block permissions
    # here we handle permissions for camera and mic and others
    opt.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1
    },)
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    if not PATH:
        driver = webdriver.Chrome(options=opt)
    else:
        driver = webdriver.Chrome(executable_path=PATH,options=opt)
    
    return driver


def get_day():
    return datetime.now().weekday()


def get_time():
    return datetime.now().time()


def login():
    global driver

    email = get_email()
    pas = get_password()

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
    #driver.find_element(By.ID, 'KmsiCheckboxField').click()      ----> for chechbox to remember our login
    driver.find_element(By.ID,'idBtn_Back' ).click()     # ---> 'idSIButton9' for clicking on yes for rember our session when we login
    time.sleep(5)
    # proceeds onto website when asked to continue on app
    driver.find_element(By.CLASS_NAME, 'use-app-lnk').click()


def join_button():
    global driver
    t = 15
    while t > 0:
        try:
            time.sleep(3)
            if not PATH:
                driver.find_element(By.XPATH, '//*[@title="Join call with video"]').click()
            else:
                driver.find_element(By.XPATH, '//*[@title="Join call with audio"]').click()
            return True
        except:
            t -= 1
            driver.refresh()
            print('Waiting for class to start....')
            time.sleep(60)
    return False


def join(sub):
    global driver
    time_now = get_time()
    #driver.find_element(By.XPATH,f'//*[@title="{sub}"]').click()
    driver.find_element(By.XPATH, f"//*[contains(text(),'{sub}')]").click()
    time.sleep(5)
    if not join_button():
        txt = f"Could not join class for {sub} till {time_now}."
        notify(txt, sub)
        print(txt)
        return False

    time.sleep(5)
    try:
        camera = driver.find_element(By.XPATH, '//toggle-button[@text = "Enable video"]')
        if camera.get_attribute('title') == 'Turn camera off':
            camera.click()
        time.sleep(3)
    except:
        print("No camera!")

    microphone = driver.find_element(By.ID, 'preJoinAudioButton')
    if microphone.get_attribute('title') == 'Mute microphone':
        microphone.click()
    time.sleep(2)

    driver.find_element(
        By.XPATH, '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button').click()
    time.sleep(2)
    txt = f"Joined class for {sub}, on {time_now}."
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
        #driver.find_element_by_xpath('//*[@id="hangup-button"]').click()
        driver.find_element(By.XPATH, '//*[@id="hangup-button"]').click()
        time.sleep(1)
        #go to home-page
        driver.find_element(By.XPATH, '//*[@id="app-bar-2a84919f-59d8-4441-a975-2a8c2643b741"]').click()
    except:
        txt = f"Could not leave meeting for {sub} on {get_time()}."
        notify(txt, sub)
        return False
    
    txt = f"Left meeting for {sub}, on {get_time()}"
    notify(txt, sub)
    return



main()
