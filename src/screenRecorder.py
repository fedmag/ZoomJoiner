#%%
import subprocess
import time
import multiprocessing

class ScreenRecorder(): # TODO https://ffmpeg.org/ffmpeg-utils.html#time-duration-syntax - exact date possible

    '''
    ffmpeg -f x11grab -s 1920x1080 -i :1.0+0,425  -f alsa -ac 2 -i hw:0  -t '10' out.mkv
    '''
    def __init__(self, output_filename) -> None: #TODO add time https://stackoverflow.com/questions/6896490/how-to-set-a-videos-duration-in-ffmpeg
        self.OUT_DIR = "/home/fedmag/Projects/ZoomJoiner/output"
        self.command = "ffmpeg -f x11grab -s 1920x1080 -i :1.0+0,425  -f alsa -ac 2 -i hw:0 -t '10' "+ self.OUT_DIR+"/" +output_filename + ".mkv"
        self.proc = None

    def ffmpeg(self):
        p = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        out = p.communicate()[0]
        self.proc = multiprocessing.Process(target=self.ffmpeg)
        return self.proc

    def run(self):
        self.proc = self.ffmpeg()
        print("ffmpeg starts recording..")
        self.proc.start()
        print("recording done!")
        print("shutting down...")
        self.proc.terminate()
        print("ffmpeg closed!")

# recorder = ScreenRecorder("test")
# recorder.run()