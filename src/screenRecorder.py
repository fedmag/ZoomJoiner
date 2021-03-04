#%%
import subprocess
import time
import multiprocessing
from configparser import ConfigParser

class ScreenRecorder(): # TODO https://ffmpeg.org/ffmpeg-utils.html#time-duration-syntax - exact date possible

    '''
    ffmpeg -f x11grab -s 1920x1080 -i :1.0+0,425  -f alsa -ac 2 -i hw:0  -t '10' out.mkv 
    -t:
    ‘55’ -> 55 seconds
    ‘12:03:45’ -> 12 hours, 03 minutes and 45 seconds
    volume:
    -filter:a "volume=1.5"
    '''
    def __init__(self, output_filename) -> None: #TODO add time https://stackoverflow.com/questions/6896490/how-to-set-a-videos-duration-in-ffmpeg
        # reading config
        config = ConfigParser()
        config.read('config.ini')
        self.OUT_DIR = config['screen_recorder']['output_dir']
        self.duration = config['screen_recorder']['default_duration']
        self.AUDIO_DEVICE = config['screen_recorder']['audio_device']
        ####################
        self.file_name = output_filename
        self.output_file_path = self.OUT_DIR + "/" + self.file_name + ".mkv"
        # self.proc = None

    def ffmpeg(self):
        record_command = f"ffmpeg -f x11grab -s 1920x1080 -i :1.0+0,425  -f pulse -i {self.AUDIO_DEVICE} -t {self.duration} {self.output_file_path}"
        p = subprocess.Popen(record_command, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        out = p.communicate()[0]
        self.proc = multiprocessing.Process(target=self.ffmpeg)
        self.proc.start()
        self.proc.terminate()
    
    # def increase_volume(self):
    #     increase_vol = "ffmpeg -i " + self.output_file_path + " -vcodec copy -af \"volume=15dB\" " + " output/increased_" + self.file_name+".mkv"
    #     p = subprocess.Popen(increase_vol, shell=True, stdout=subprocess.PIPE,
    #                      stderr=subprocess.PIPE)
    #     out = p.communicate()[0]
    #     self.proc = multiprocessing.Process(target=self.increase_volume)
    #     self.proc.start()
    #     self.proc.terminate()


    def run(self):
        print("ffmpeg starts recording..")
        self.ffmpeg()
        # self.proc.start()
        print("recording done!")
        print("shutting down...")
        # self.proc.terminate()
        print("ffmpeg closed!")
        # print("increasing volume...")
        # self.increase_volume()
        # print("volume increased")

# recorder = ScreenRecorder("try")
# recorder.run()