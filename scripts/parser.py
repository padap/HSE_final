import re
import requests
import os, sys
from tqdm import tqdm, tqdm_notebook

import time
import youtube_dl
import pickle
import shutil


RESTTIME = 5
DATAFOLDER = '../data/'
NUM_OF_VIDEO = 100#None
if not os.path.exists(DATAFOLDER):
    os.mkdir(DATAFOLDER)
    
def get_urls(fn = 'urls.txt'):
    lst = open(fn, 'r', encoding="utf-8").read().split('\n')
    res = {i.split('	')[0]:float(i.split('	')[1]) for i in lst}
    return res

def load_single_video(url):
    result = False
    try:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
        result = True
    except:
        sys.stderr.write("Can't load video %s"%url)
        time.sleep(RESTTIME*30)
        
url_list = [i[0] for i in sorted(get_urls().items(), key = lambda x:-x[1])]

if NUM_OF_VIDEO is not None:
    url_list = url_list[:NUM_OF_VIDEO]

for url in tqdm(url_list):
    files_old = os.listdir('.')
    load_single_video(url)
    files_new = os.listdir('.')
    files = list(set(files_new)-set(files_old))
    if len(files)!=1:
        sys.stderr.write('Something wrong, there are several files :\n'+str(files))
    else:
        fn = files[0]
        shutil.move(fn, DATAFOLDER+fn)
    time.sleep(RESTTIME)