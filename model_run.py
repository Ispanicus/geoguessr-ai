import numpy as np
import torch
import clip
import os
from PIL import Image
import numpy as np
from collections import OrderedDict
import pickle
import random

model, preprocess = clip.load("ViT-L/14")
model.cuda().eval()
input_resolution = model.visual.input_resolution
context_length = model.context_length
vocab_size = model.vocab_size

print("Model parameters:", f"{np.sum([int(np.prod(p.shape)) for p in model.parameters()]):,}")
print("Input resolution:", input_resolution)
print("Context length:", context_length)
print("Vocab size:", vocab_size)

image_src = "../geodata/mapillary1" 
batch_size = 1000
data = pickle.load(open(f"../geodata/metadata_w_google.pickle","rb"))
file_country = {}
for key in data.keys():
    for i in range(len(data[key]["results"])):
        if "country" in data[key]["results"][i]["types"]:
            country = data[key]["results"][i]["address_components"][0]["long_name"]
            file_country[key] = country

def get_data(batch_size = 1000, image_src = "", text_data = {},verbose=False,final_batch=True):
    max_batch_num = len(os.listdir(f"{image_src}"))//batch_size
    remainder = len(os.listdir(f"{image_src}"))%batch_size
    for batch_num in range(max_batch_num+1):
        
        images = []
        texts = []
        
        if batch_num == max_batch_num and remainder == 0:
            continue
        elif batch_num == max_batch_num and final_batch == True:
            filenames = [filename for filename in os.listdir(f"{image_src}")[max_batch_num*batch_size::] if filename.endswith(".jpg")]
        elif batch_num == max_batch_num and final_batch != True:
            continue
        else:
            filenames = [filename for filename in os.listdir(f"{image_src}")[batch_num*batch_size:(batch_num+1)*batch_size] if filename.endswith(".jpg")]
        
        for filename in filenames:
            name = os.path.splitext(filename)[0]
            if name not in text_data:
                if verbose: print("missing: ", name)
                continue
                
            image = Image.open(f"{image_src}/{filename}").convert("RGB")


            if name in file_country:
                images.append(preprocess(image))
                texts.append(text_data[name])
            else:
                error_name_list.append(name)
                
        yield images, texts, filenames
    
    
def convert_from_desc(text,start_text,end_text):
    text = text.replace(start_text, "")
    text = text.replace(end_text, "")
    return text


all_labels = []
all_texts = []
for images, texts, filenames in get_data(batch_size = 1000, image_src = image_src, text_data = file_country):
    print("Got batch number: ", batch)
    combined = list(zip(images, texts, filenames))
    random.shuffle(combined)
    images[:], texts[:], filenames[:] = zip(*combined)
    image_input = torch.tensor(np.stack(images)).cuda()
    start_text = "This is a photo of "
    end_text = ", a country"
    text_descriptions = [f"{start_text}{cc}{end_text}" for cc in set(file_country.values())]
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

outdict = dict()
outdict[true_texts] = all_texts
outdict[predict_texts] = top_label_text

with open("results.pickle", 'wb') as handle:
    pickle.dump(outdict, handle, protocol=pickle.HIGHEST_PROTOCOL)
