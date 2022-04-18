import csv
# from sklearn.metrics import classification_report,confusion_matrix
# from sklearn.metrics import matthews_corrcoef as MC
# from sklearn.metrics import ConfusionMatrixDisplay as CMD
# import matplotlib.pyplot as plt
# from collections import Counter as Cnt
import geopandas as gpd
# import pickle
import pandas as pd
# import json
# import random
from PIL import Image


def read_resultcsv(result_file):
    """Input: result_file name of csv file
    Returns: 
        gold: list of true values
        predicts: list of lists of top5 predictions
        probs: list of lists of top5 probabilities
        filenames: list of filenames for input images
        """
    labelspair = []

    with open(f'../resultcsv/{result_file}', encoding="utf-8",newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            if row[0]=="Gold":
                continue
            gold = row[0]
            preds = row[1][2:-2].split(", ")
            preds = [x.strip("'") for x in preds]
            probs = row[2][2:-2].split(", ")
            probs = [float(x) for x in probs]
            filename = row[3]
            labelspair.append([gold,preds,probs,filename])
                    
    gold = [x[0] for x in labelspair]
    predicts = [x[1] for x in labelspair]
    probs = [x[2] for x in labelspair]
    filenames = [x[3] for x in labelspair]
                        
    return gold, predicts, probs, filenames

def read_georesultcsv(result_file):
    """Input: result_file name of geoestimation csv file
    Returns: 
        grade_img_pred dictionary
        first key is "grade" of prediction i.e coarse, middle etc
        second key is img_id (without .jpg extension)
        result is dictionary with pred_lat, pred_lon, pred_class keys
        """
    grade_img_pred = {}

    with open(f'../georesultcsv/{result_file}', encoding="utf-8",newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        
        for row in reader:
            row = row[0].split(",")
            if row[0]=="img_id":
                continue
            img_id = row[0]
            p_key = row[1]
            pred_class = row[2]
            pred_lat = row[3]
            pred_lng = row[4]
            grade_img_pred.setdefault(p_key,{})
            grade_img_pred[p_key][img_id] = {"pred_lat":pred_lat,
                                             "pred_lon":pred_lng,
                                             "pred_class":pred_class
                                            }
                    
                        
    return grade_img_pred

def filter_classes(gold,predict,selection):
    """ Given selection of classes filter all other classes to "other" to allow easier display for confusion matrix
            Input:
                    gold: list of true labels
                    predict: list of predictions (i.e top1 prediction from predicts)
                    selection: list of classes to include
            Output:
                    goldsel: list of true labels with filtered classes changed to "other" 
                    predsel: list of predictions with filtered classes changed to "other" """
    goldsel = []
    predsel = []
    for g, p in zip(gold,predict):

        if g in selection:
            if p in selection:
                    goldsel.append(g)
                    predsel.append(p)
            else:
                    p = "other"
                    goldsel.append(g)
                    predsel.append(p)
        else:
            g = "other"
            if p in selection:
                    goldsel.append(g)
                    predsel.append(p)
            else:
                    continue
    return goldsel, predsel

def filter_classes_one(gold,predict,selection):
    """ Given single class "selection" filter all other classes to "other" if there are no false positive or false negatives involving those classes and the selection. This allows qualitative analysis of single class
        Input:
                gold: list of true labels
                predict: list of predictions (i.e top1 prediction from predicts)
                selection: string of selected class
        Output:
                goldsel: list of true labels with filtered classes changed to "other" 
                predsel: list of predictions with filtered classes changed to "other"
                indices: list of indices which helps find relevant image files"""
                        
    goldsel = []
    predsel = []
    indices = []
    for i, (g, p) in enumerate(zip(gold,predict)):

        if g == selection or p == selection:
            indices.append(i)
            goldsel.append(g)
            predsel.append(p)
        else:
            g = "other"
            if p == selection:
                indices.append(i)
                goldsel.append(g)
                predsel.append(p)
            else:
                continue
                            
    return goldsel, predsel, indices

def get_data(batch_size = 1000, image_src = None , inputcsv_src  = None , verbose=False , final_batch=True):
    """Requires:
    image_src: path to directory with all images e.g /home/data_shares/mapillary/train for HPC
    inputcsv_src: path to input csv file e.g ../inputdata/France_states_max100.csv

    yields:
    list of images that have been opened and converted to RGB
    list of texts which are labels for each image
    list of filenames without .jpg extension"""
        
    files = []
    file_label_dict = {}
    with open(inputcsv_src, encoding="utf-8",newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            files.append(row[0])
            file_label_dict[row[0]] = row[1]
        
        
    max_batch_num = len(files)//batch_size
    remainder = len(files)%batch_size
    for batch_num in range(max_batch_num+1):
        
        images = []
        texts = []
        
        if batch_num == max_batch_num and remainder == 0:
            continue
        elif batch_num == max_batch_num and final_batch == True:
            filenames = [filename for filename in files[max_batch_num*batch_size::]]
        elif batch_num == max_batch_num and final_batch != True:
            continue
        else:
            filenames = [filename for filename in files[batch_num*batch_size:(batch_num+1)*batch_size] ]
        
        for filename in filenames:            
            image = Image.open(f"{image_src}/{filename}.jpg").convert("RGB")
            images.append(preprocess(image))
            texts.append(file_label_dict[filename])
                        
        yield images, texts, filenames
                
def convert_from_desc(text,start_text,end_text):
    """Returns text with start_text removed from start and end_text removed from end of text string"""
    text = text.replace(start_text, "")
    text = text.replace(end_text, "")
    return text
    
def country_from_coords(filenamelist, latlist, lonlist):
    """Takes in 3 lists: filenamelist, latlist, longlist 
    returns a dictionary with filename:country"""
    countrydf = gpd.read_file("../SHP/Countries/world-administrative-boundaries.shp", encoding="utf-8")
    coords = pd.DataFrame({'Filename':filenamelist, 'Latitude': latlist, 'Longitude': lonlist})
    coordsdf = gpd.GeoDataFrame(coords, crs=4326, geometry=gpd.points_from_xy(coords.Longitude, coords.Latitude))
    countrycoorddf = gpd.sjoin(coordsdf, countrydf)
    countrydict = dict()
    for row in countrycoorddf.iterrows():
        countrydict[row[1][0]] = row[1][10]
    return countrydict