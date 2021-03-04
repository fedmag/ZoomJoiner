#%%
'''
get the day and link from a csv file.
click the link 
start screen recording
'''
import configparser
import pandas as pd
from selenium import webdriver 
# from selenium.webdriver.common.keys import Keys
import pyautogui
import time
import psutil
from datetime import datetime
from configparser import ConfigParser
from screenRecorder import ScreenRecorder

class ZoomJoiner():

    def __init__(self, zoom_path=None) -> None:
        # reading config.ini
        config = ConfigParser()
        config.read("config.ini")
        data_csv_path = config['zoom_joiner']['data_path']
        self.WEB_DRIVER_PATH = config['zoom_joiner']['firefox_web_driver_path']
        self.FIREFOX_PATH = config['zoom_joiner']['firefox_path'] 
        self.ZOOM_PATH = zoom_path
        # reading data
        self.data = pd.read_csv(data_csv_path)
        self.WEEKDAYS = {"Monday" : 1, "Tuesday" : 2, "Wednesday" : 3, "Thursday" : 4, "Friday" : 5, "Saturday" : 6, "Sunday" : 7}
        # selenium options
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument("--test-type")
        self.options.binary_location = self.FIREFOX_PATH # set path to browser file
        self.driver = None    

    def check_meetings(self):
        for i, row in self.data.iterrows():
            meeting_day = row['day']
            now = datetime.now()
            meeting_time = row['time']
            if self.WEEKDAYS[meeting_day] == now.isoweekday(): # checking that we have a meeting today #TODO dont print if the meeting was in the past the same day
                print(f"There is a meeting scheduled for {meeting_day} at {meeting_time}.")
                now = self.get_current_time()
                print(f"current time: {now}, meeting time: {meeting_time}")
                if meeting_time == now: # we have a meeting starting
                    print(f"Meeting \"{row['subject']}\" is starting...")
                    self.join_zoom(row['meeting_link'], row['subject'])
    
    def get_current_time(self):
        now = datetime.now()
        now = now.ctime()
        now = now.split(" ")
        time = now[4]
        time = time.split(":")
        time = time[0] + ":" + time[1]
        return time
                
    def join_zoom(self, link, meeting_name, meeting_id=None, meeting_psw=None):
        self.driver = webdriver.Firefox(executable_path=self.WEB_DRIVER_PATH)
        self.driver.get(link)
        time.sleep(5)
        try:
            open_app_btn_x, open_app_btn_y = pyautogui.locateCenterOnScreen("data/imgs/open_zoom_btn_firefox.png")
            pyautogui.click(open_app_btn_x, open_app_btn_y)
            time.sleep(2)
            open_app_btn_x, open_app_btn_y = pyautogui.locateCenterOnScreen("data/imgs/confirmation_btn_firefox.png")
            pyautogui.click(open_app_btn_x, open_app_btn_y)
        except:
            print("The button couldn't be located on the screen")
            self.log_using_manual_data(meeting_id, meeting_psw)
        self.close_driver()
        self.record_screen(meeting_name)

    def record_screen(self, output_file_name: str):
        recorder = ScreenRecorder(output_file_name)
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

    
    
zoom_joiner = ZoomJoiner()
while True:
    zoom_joiner.run()
    time.sleep(59)
# %%
