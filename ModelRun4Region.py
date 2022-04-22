# The purpose of this file is to use the region_to_country json file to select which countries are going to be options for the model to pick from

import os; print(os.environ['CONDA_DEFAULT_ENV'])
import numpy as np
import torch
import clip
import sys
import csv
import json
from PIL import Image
from collections  import OrderedDict
# import pickle
import random
from pathlib import Path
from Utils import convert_from_desc,read_resultcsv
# from tqdm import tqdm
# from sklearn.metrics import f1_score
# from sklearn.metrics import precision_recall_fscore_support as prfs

model_name = 'ViT-L/14'
model, preprocess = clip.load(model_name)
model.cuda().eval()
input_resolution = model.visual.input_resolution
context_length = model.context_length
vocab_size = model.vocab_size

print("Model name: ",model_name)
print("Input resolution:", input_resolution)
print("Context length:", context_length)
print("Vocab size:", vocab_size);
print("____________________________")

print("First arg, (image source) = ", sys.argv[1])
print("Second arg, (file-label list) = ", sys.argv[2])

# prompt_dict = {
#     "UScity100" : "American city" ,
#     "US_states_max100": "state",
#     "France_states_max100": "French state" ,
#     "city100": "city" ,
#     "city300": "city" ,
#     "country100": "country" ,
#     "country100": "country" ,

# }
img_src = sys.argv[1]
files_src = sys.argv[2]
prompt = "country" #prompt_dict[Path(files_src).stem]
start_text = "This is a photo of "
end_text = f", a {prompt}"

    
with open("../pickles/country_to_region.json", encoding="utf-8") as file:
    region_to_country = json.load(file)
with open(files_src) as f:
    length_of_input = sum(1 for line in f)
    
def get_data(batch_size = 1000, image_src = None , inputcsv_src  = None , verbose=False , final_batch=True):
    """Requires:
    image_src: path to directory with all images e.g /home/data_shares/mapillary/train for HPC
    inputcsv_src: path to input csv file e.g ../inputdata/France_states_max100.csv

    yields:
    list of images that have been opened and converted to RGB
    list of texts which are labels for each image
    list of filenames without .jpg extension"""
    # model_name = 'ViT-L/14'
    # model, preprocess = clip.load(model_name)
    # model.cuda().eval()
    
    _, predicts, _, filenames = read_resultcsv(inputcsv_src)
    files = []
    file_label_dict = {}
    for predict,filename in zip(predicts,filenames):
        files.append(filename)
        file_label_dict[filename]=predict[0]
        
        
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
batch = 0
batch_size = 1
all_labels = []
all_texts = []
all_probs = []
all_filenames = []
for images, texts, filenames in get_data(batch_size = batch_size, image_src = img_src, inputcsv_src = files_src):
    savefilename = f"../progress/{os.path.basename(files_src[:-4])}_progress.out"
    with open(savefilename, "w") as progressfile:
        progressfile.write(f"Progress: {100*batch*batch_size/length_of_input}%")
    batch += 1
    combined = list(zip(images, texts, filenames))
    #random.shuffle(combined)
    images[:], texts[:], filenames[:] = zip(*combined)
    image_input = torch.tensor(np.stack(images)).cuda()

    text_descriptions = [f"{start_text}{cc}{end_text}" for cc in region_to_country[texts[0]] #get list of countries to guess from since batch=1 texts should have 1 region in it
    text_tokens = clip.tokenize(text_descriptions).cuda()
    
    with torch.no_grad():
        image_features = model.encode_image(image_input).float()
        text_features = model.encode_text(text_tokens).float()
        text_features /= text_features.norm(dim=-1, keepdim=True)
        
    text_probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)
    topk = 1 # changed to 1 since not all regions have more than 1 guess
    top_probs, top_labels = text_probs.cpu().topk(topk, dim=-1)
    all_labels.extend([[label.item() for label in image] for image in top_labels])
    all_probs.extend([[prob.item() for prob in image] for image in top_probs])
    all_texts.extend(texts)
    all_filenames.extend(filenames)
    

top_label_text = [[convert_from_desc(text_descriptions[labels[x]],start_text,end_text) for x in range(len(labels))] for labels in all_labels]

savefilename = f"../resultcsv/{os.path.basename(files_src[:-4])}_results.csv"
print("savefilename: ", savefilename)
with open(savefilename,'w', encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(["Gold","Predictions", "Probabilities"])
    output = [[x,y,z,z2] for x,y,z,z2 in zip(all_texts,top_label_text,all_probs,all_filenames)]
    for row in output:
        writer.writerow(row)

