# ! pip install ftfy regex tqdm;
# ! pip install git+https://github.com/openai/CLIP.git;
import numpy as np
import torch
import clip
import os
import sys
import csv
from PIL import Image
from collections  import OrderedDict
# import pickle
import random
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
print("Third arg, (label type) = ", sys.argv[3])

arg3 = sys.argv[3]
start_text = "This is a photo of "
end_text = f", a {arg3}"

img_src = sys.argv[1]
files_src = sys.argv[2]

files = []
file_label_dict = {}
with open(files_src, encoding="utf-8",newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        files.append(row[0])
        file_label_dict[row[0]] = row[1]


def get_data(batch_size = 1000, image_src = img_src, text_data = {},verbose=False,final_batch=True):
    """Requires:
    image_src which is path to directory with all images
    text_data which is dictionary with filename:label key-value pairs

    yields:
    list of images that have been opened and converted to RGB
    list of texts which are labels for each image
    list of filenames without .jpg extension"""
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
            texts.append(text_data[filename])
                
        yield images, texts, filenames
    
    
def convert_from_desc(text,start_text,end_text):
    text = text.replace(start_text, "")
    text = text.replace(end_text, "")
    return text


batch = 0
all_labels = []
all_texts = []
for images, texts, filenames in get_data(batch_size = 1000, image_src = img_src, text_data = file_label_dict):
    print("Got batch number: ", batch)
    combined = list(zip(images, texts, filenames))
    random.shuffle(combined)
    images[:], texts[:], filenames[:] = zip(*combined)
    image_input = torch.tensor(np.stack(images)).cuda()

    text_descriptions = [f"{start_text}{cc}{end_text}" for cc in set(file_label_dict.values())]
    text_tokens = clip.tokenize(text_descriptions).cuda()
    
    with torch.no_grad():
        image_features = model.encode_image(image_input).float()
        text_features = model.encode_text(text_tokens).float()
        text_features /= text_features.norm(dim=-1, keepdim=True)
        
    text_probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)
    top_probs, top_labels = text_probs.cpu().topk(1, dim=-1)
    all_labels.extend([[label.item() for label in image] for image in top_labels])
    all_texts.extend(texts)
    

top_label_text = [[convert_from_desc(text_descriptions[labels[x]],start_text,end_text) for x in range(len(labels))] for labels in all_labels]

savefilename = f"{os.path.basename(files_src[:-4])}_results.csv"
with open(savefilename,'w', encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Gold","Predict"])
    output = [[x,y[0]] for x,y in zip(all_texts,top_label_text)]
    for row in output:
        writer.writerow(row)

