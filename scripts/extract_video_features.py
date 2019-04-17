#add gpu calculation
#add batch loading images

import os, sys
from tqdm import tqdm, tqdm_notebook
import pickle
import time
import numpy as np
from keras.applications.vgg16 import decode_predictions
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import VGG16
model = VGG16()
#from matplotlib import pyplot as plt
#%matplotlib inline

from keras import backend as K

# with a Sequential model
nn_3_way    = K.function([model.layers[1].input],
                         [model.layers[-1].output, 
                          model.layers[-2].output, 
                          model.layers[-3].output])

FEATURENAMES = ['-1', '-2', '-3']

def _get_image(fn):
    image = load_img(fn, target_size=(224, 224))
    image = img_to_array(image)
    image = preprocess_input(image)
    return image

def _get_batch(fn_list):
    image_array = []
    for fn in tqdm(fn_list):
        image_array.append(_get_image(fn))
    return np.array(image_array)

def make_features(y_pred):
    shape = y_pred.shape[1]
    funct_dict = {'mean'  : lambda x: np.mean(x, axis = 0).reshape(1, shape),
                  'med'   : lambda x: np.median(x, axis = 0).reshape(1, shape),
                  'std'   : lambda x: np.std(x, axis = 0).reshape(1, shape),
                  'minmax' :lambda x: (np.max(x, axis = 0)-np.mean(x, axis = 0)).reshape(1, shape)}
        
    res = {funct_name : funct(y_pred) for funct_name, funct in funct_dict.items()}
    
    return res

def _predict(X, save_raw = True):
    #!!!!
    #Make batch realization, now it's all folder, there would be problem, with GPU RAM
    nn_prediction = nn_3_way([X])
    res = {name: feature for name, feature in zip(FEATURENAMES, nn_prediction)}

    res_final = {'features' : {name : make_features(y_pred) for name, y_pred in res.items()}
                }
    
    if save_raw:
        res_final['raw'] = res.copy()
        
    return res_final

def calculate_features_for_one_folder(folder_name, save_raw = False):
    fn_list = [folder_name+i for i in os.listdir(folder_name)]
    X = _get_batch(fn_list)
    res = _predict(X, save_raw = save_raw)
    return res

def run(folder_video_prefix, save_raw = False):
    folders = ['../features/', '../features/video']
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)
            
    for video_id in tqdm(os.listdir(folder_video_prefix)):
        if not os.path.exists('../features/video/'+video_id+'/'):
            os.mkdir('../features/video/'+video_id+'/')
            
        folder_name_id = folder_video_prefix+video_id
        for segm_id in os.listdir(folder_name_id):
    
            folder_name_segm = folder_name_id+'/'+segm_id
            ID = int(segm_id)
            res = calculate_features_for_one_folder(folder_name_segm+'/', )
            
            #save result
            pickle.dump(res, open('../features/video/'+video_id+'/%04d.pickle'%ID, 'wb'))

run('../segm/video/')