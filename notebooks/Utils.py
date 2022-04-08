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