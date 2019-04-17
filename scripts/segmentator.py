from moviepy.editor import *
from multiprocessing import Process
#from moviepy import editor
from tqdm import tqdm, tqdm_notebook
import time
from importlib import reload  # Python 3.4+ only.

import os, sys, pickle
from tqdm import tqdm, tqdm_notebook

#Create directories
PREF = '../segm/'
    
PREF_AUDIO = PREF+'audio/'
PREF_VIDEO = PREF+'video/'

for pref in [PREF, PREF_AUDIO, PREF_VIDEO]:
    if not os.path.exists(pref):
        os.mkdir(pref)
        
SEGMENT_LENGTH = 2
FPS_RATE = 30

def parseId(fn):
    return fn[-15:-4]

def segment_single_video(fn):
    video = VideoFileClip(fn)
    
    duration = video.duration
    num_of_segments = int(duration / SEGMENT_LENGTH)
    start_pos = (duration - num_of_segments*2)/2

    ID = parseId(fn)
    for path in [PREF_AUDIO+ID, PREF_VIDEO+ID]:
        if not os.path.exists(path):
            os.mkdir(path)
            
    for segment_id in tqdm(range(num_of_segments)):
        start_time = start_pos+segment_id*SEGMENT_LENGTH
        end_time = start_time+SEGMENT_LENGTH
        subvideo = video.subclip(start_time, end_time)

        #Write audio file to '../segm/audio/{ID}/(segm_id).mp3'
        audio_file = PREF_AUDIO+ID+'/%04d.mp3'%(segment_id)
        subvideo.audio.write_audiofile(audio_file, verbose = False)
        
        #Write pictures to '../segm/video/{ID}/(segm_id)/{frame}.jpeg'
        video_folder = PREF_VIDEO+ID+'/%04d/'%(segment_id)
        if not os.path.exists(video_folder):
            os.mkdir(video_folder)
            
        video_folder = video_folder +'%04d.jpeg'
        subvideo.write_images_sequence(video_folder, fps = FPS_RATE, verbose = False)

            

def simple_filter(s):
    if s[-4:] == '.mp4':
        return True
    return False


for fn in tqdm(['../data/'+i for i in os.listdir('../data')]):
    if not simple_filter(fn):
        sys.stderr.write('!!!!! Something wrong with file '+fn)
        continue
    
    segment_single_video(fn)
    