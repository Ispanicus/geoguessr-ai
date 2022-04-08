import csv
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import matthews_corrcoef as MC
from sklearn.metrics import ConfusionMatrixDisplay as CMD
import matplotlib.pyplot as plt
from collections import Counter as Cnt
import geopandas as gpd
import pickle
import pandas as pd
import json
import random



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

        if g == selection:
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
    