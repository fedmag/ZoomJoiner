#%%
'''
get the day and link from a csv file.
click the link 
start screen recording
'''
import pandas as pd
from selenium import webdriver 
# from selenium.webdriver.common.keys import Keys
import pyautogui
import time
import psutil
from datetime import datetime
from configparser import ConfigParser
from screenRecorder import ScreenRecorder
import os
import utils

class ZoomJoiner():

    def __init__(self, zoom_path=None) -> None:
        # reading config.ini
        self.project_dir = utils.get_project_dir()
        config = ConfigParser()
        config.read(self.project_dir + "/config.ini")
        self.data_csv_path = config["zoom_joiner"]["data_path"]
        self.WEB_DRIVER_PATH = config['zoom_joiner']['firefox_web_driver_path']
        self.FIREFOX_PATH = config['zoom_joiner']['firefox_path'] 
        self.ZOOM_PATH = config['zoom_joiner']['zoom_path']
        # reading data
        self.data = pd.read_csv(self.data_csv_path)
        self.WEEKDAYS = {"monday" : 1, "tuesday" : 2, "wednesday" : 3, "thursday" : 4, "friday" : 5, "saturday" : 6, "sunday" : 7}
        # selenium options
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument("--test-type")
        self.options.binary_location = self.FIREFOX_PATH # set path to browser file
        self.driver = None 
        self.recording = False 
        #################  
        self.debug = False

    def check_meetings(self) -> None:
        for i, row in self.data.iterrows():
            meeting_day = row['day']
            meeting_day = meeting_day.strip().lower()
            now = datetime.now()
            meeting_time = row['time']
            if self.WEEKDAYS[meeting_day] == now.isoweekday(): # checking that we have a meeting today #TODO dont print if the meeting was in the past the same day
                now = utils.get_current_time()
                print(f"There is a meeting scheduled at {meeting_time}, current time {now}.")
                if meeting_time == now: # we have a meeting starting
                    print(f"Meeting \"{row['subject']}\" is starting...")
                    self.join_zoom(row['meeting_link'], row['subject'])
                   
    def join_zoom(self, link, meeting_name, meeting_id=None, meeting_psw=None) -> None:
        self.driver = webdriver.Firefox(executable_path=self.WEB_DRIVER_PATH)
        self.driver.get(link)
        time.sleep(5)
        try:
            open_app_btn_x, open_app_btn_y = pyautogui.locateCenterOnScreen(self.project_dir+"/data/imgs/open_zoom_btn_firefox.png")
            pyautogui.click(open_app_btn_x, open_app_btn_y)
            time.sleep(2)
            open_app_btn_x, open_app_btn_y = pyautogui.locateCenterOnScreen(self.project_dir+"/data/imgs/confirmation_btn_firefox.png")
            pyautogui.click(open_app_btn_x, open_app_btn_y)
        except:
            print("The button couldn't be located on the screen")
            self.log_using_manual_data(meeting_id, meeting_psw)
        self.close_driver()
        self.record_screen(meeting_name)

    def record_screen(self, meeting_name: str) -> None:
        date = utils.get_current_date()
        output_file_name = meeting_name + date
        self.recording = True
        recorder = ScreenRecorder(output_file_name)
        recorder.run()
        self.recording = False

    def log_using_manual_data(self, meeting_id, meeting_psw) -> None: #TODO log in using meetingID and meetingPSW
        pass

    def close_driver(self) -> None:
        driver_process = psutil.Process(self.driver.service.process.pid)
        firefox_process = driver_process.children()        
        self.driver.close()
        self.driver.quit()
        if firefox_process[0].is_running():
            print(firefox_process[0])
            firefox_process[0].kill()
    
    def meeting_ended_popup(self) -> None:
        try:
            open_app_btn_x, open_app_btn_y = pyautogui.locateCenterOnScreen(self.project_dir+"/data/imgs/ok_button.png")
            pyautogui.click(open_app_btn_x, open_app_btn_y)
        except:
            if not self.recording:
                if self.debug:
                    print("No popup detected!")
    
    def update_data(self) -> None:
        self.data = pd.read_csv(self.data_csv_path)

    def run(self) -> None:
        print("==============================")
        self.check_meetings()
        self.update_data()
        self.meeting_ended_popup()
        print("==============================")
  
    
zoom_joiner = ZoomJoiner()
while True:
    zoom_joiner.run()
    time.sleep(30)
# %%

