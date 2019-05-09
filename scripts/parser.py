from pytube import YouTube
import time
import sys
from tqdm import tqdm 

RESTTIME      = 30
urls_filename = 'urls.txt'
output_path   = '../data/'
max_urls      = 300


def get_id_from_url(url):
    return url[-11:]

def load_single_video(url, rest_time, 
                      output_path, verbose):
    result = False
    ID = get_id_from_url(url)
    try:
        t = YouTube(url).streams.first()
        if verbose:
            print(url)
            print(t.fmt_profile)
        filename = ID+'('+t.default_filename[:-3]+')'
        t.download(output_path=output_path, filename = filename)
        result = True
        print('Ok')        
        time.sleep(rest_time)
    except:
        sys.stderr.write("\n\nCan't load video %s \n"%url)
        time.sleep(rest_time*5)
        result = False
    return result

if __name__ == "__main__":
    urls_list = open(urls_filename, 'r').read().split('\n')[::-1]
    for url in tqdm(urls_list[:max_urls]):
        print(url)
        result = load_single_video(url, 
                                   rest_time=RESTTIME, 
                                   output_path=output_path,
                                   verbose = 1)
        del YouTube
        from pytube import YouTube


# import re
# import requests
# import os, sys
# from tqdm import tqdm, tqdm_notebook

# import time
# import youtube_dl
# import pickle
# import shutil


# RESTTIME = 2
# DATAFOLDER = '../data/'
# NUM_OF_VIDEO = 10#None
# if not os.path.exists(DATAFOLDER):
#     os.mkdir(DATAFOLDER)
    
# def get_urls(fn = 'urls.txt'):
#     lst = open(fn, 'r', encoding="utf-8").read().split('\n')
#     if '	' in lst[0]:
#         res = {i.split('	')[0]:float(i.split('	')[1]) for i in lst}
#     else:
#         res = {i:6.66e7 for i in lst}
        
#     return res

# def load_single_video(url):
#     result = False
#     try:
#         ydl_opts = {}
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#                     ydl.download([url])
#         result = True
#     except:
#         sys.stderr.write("Can't load video %s"%url)
#         time.sleep(RESTTIME*30)

# url_list = [i[0] for i in sorted(get_urls().items(), key = lambda x:-x[1])]

# if NUM_OF_VIDEO is not None:
#     url_list = url_list[:NUM_OF_VIDEO]

# for url in tqdm(url_list):
#     files_old = os.listdir('.')
#     load_single_video(url)
#     files_new = os.listdir('.')
#     files = list(set(files_new)-set(files_old))
#     if len(files)!=1:
#         sys.stderr.write('Something wrong, there are several files :\n'+str(files))
#     else:
#         fn = files[0]
#         shutil.move(fn, DATAFOLDER+fn)
#     time.sleep(RESTTIME)