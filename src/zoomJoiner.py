#%%
'''
get the day and link from a csv file.
click the link 
start screen recording
'''
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import pyautogui
import time
import psutil
from datetime import datetime
from screenRecorder import ScreenRecorder

class ZoomJoiner():

    def __init__(self, data_csv_path, zoom_path=None) -> None:
        self.data = pd.read_csv(data_csv_path)
        self.ZOOM_PATH = zoom_path
        self.WEEKDAYS = {"Monday" : 1, "Tuesday" : 2, "Wednesday" : 3, "Thursday" : 4, "Friday" : 5, "Saturday" : 6, "Sunday" : 7}
        # selenium options
        self.options = webdriver.FirefoxOptions()
        # self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument("--test-type")
        # self.options.headless = True # do not open the browser 
        self.options.binary_location = "/usr/bin/firefox" # set path to browser file
        self.driver = None    

    def check_meetings(self):
        for i, row in self.data.iterrows():
            meeting_links = row['meeting_link']
            meeting_day = row['day']
            now = datetime.now()
            meeting_hr_complete = row['time']
            meeting_hr_splits = meeting_hr_complete.split(":") 
            meeting_hr = meeting_hr_splits[0]
            meeting_min = meeting_hr_splits[0]
            if self.WEEKDAYS[meeting_day] == now.isoweekday(): # checking that we have a meeting today #TODO dont print if the meeting was in the past the same day
                print(f"There is a meeting scheduled for {meeting_day} at {meeting_hr_complete}.")
                now_hr = str (now.hour) + ":" + str(now.minute)
                print(f"current time: {now_hr}, meeting time: {meeting_hr_complete}")
                if meeting_hr_complete == now_hr: # we have a meeting starting
                    print(f"Meeting \"{row['subject']}\" is starting...")
                    self.join_zoom(row['meeting_link'])
                
    def join_zoom(self, link, meeting_id=None, meeting_psw=None):
        self.driver = webdriver.Firefox(executable_path="/home/fedmag/Projects/ZoomJoiner/lib/geckodriver")
        self.driver.get(link)
        time.sleep(5)
        try:
            open_app_btn_x, open_app_btn_y = pyautogui.locateCenterOnScreen("/home/fedmag/Projects/ZoomJoiner/data/imgs/open_zoom_btn_firefox.png")
            pyautogui.click(open_app_btn_x, open_app_btn_y)
            time.sleep(2)
            open_app_btn_x, open_app_btn_y = pyautogui.locateCenterOnScreen("/home/fedmag/Projects/ZoomJoiner/data/imgs/confirmation_btn_firefox.png")
            pyautogui.click(open_app_btn_x, open_app_btn_y)
        except:
            print("The button couldn't be located on the screen")
            self.log_using_manual_data(meeting_id, meeting_psw)
        self.close_driver()
        self.record_screen()

    def record_screen(self):
        recorder = ScreenRecorder("real_test")
        recorder.run()

    def log_using_manual_data(self, meeting_id, meeting_psw): #TODO log in using meetingID and meetingPSW
        pass

    def close_driver(self):
        driver_process = psutil.Process(self.driver.service.process.pid)
        firefox_process = driver_process.children()        
        self.driver.close()
        self.driver.quit()
        if firefox_process[0].is_running():
            print(firefox_process[0])
            firefox_process[0].kill()

    def run(self):
        self.check_meetings()

    
    
zoom_joiner = ZoomJoiner("/home/fedmag/Projects/ZoomJoiner/data/timetable.csv")
while True:
    zoom_joiner.run()
    time.sleep(59)
# %%
# now = datetime.now()
# now.
# %%
