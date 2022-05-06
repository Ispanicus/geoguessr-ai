import os
import clip
import json
import csv
import sys
from multiprocessing import Pool
from pathlib import Path


caption_files = []
for x in range(32):
    suffix = str(x+1)
    if len(suffix) == 1:
        suffix="0"+suffix
    caption_files.append("/home/data_shares/mapillary/cah400M/cah400M"+suffix+".txt")

inputfile = sys.argv[1]

label_to_tokens = {}

with open(inputfile, encoding="utf-8",newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        label = row[1]
        if label in label_to_tokens.keys():
            continue
        else:

            tokens_set = set(clip.tokenize(label).numpy()[0])
            label_to_tokens[label]=tokens_set

def LAION_label_count(caption_file):
    label_count = {label:0 for label in label_to_tokens.keys()} 
    
    with open(caption_file,encoding="utf-8") as capfile:
        for caption in capfile:
            try:
                # Due to context length issues some of the captions will be skipped
                caption_tokens_set = set(clip.tokenize(caption).numpy()[0])
            except:
                continue
            for key in label_to_tokens.keys():
                tokens = label_to_tokens[key]
                if tokens.issubset(caption_tokens_set):
                    label_count[key] += 1
    os.mkdir(f"../label_counts/{Path(inputfile).stem}")
    with open(f"../label_counts/{Path(inputfile).stem}/{Path(inputfile).stem}_tokens_labelcount{idx}.json", 'w',encoding="utf-8") as handle:
        json.dump(label_count, handle, ensure_ascii=False,indent=4)
    return label_count



def main():
    with Pool(32) as p:
        p.map(LAION_label_count,caption_files)


if __name__ == "__main__":
    main()