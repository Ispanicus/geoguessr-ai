
import os
import clip
import json
import csv
from tqdm import trange
from multiprocessing import Pool


# model_name = 'ViT-L/14'
# model, preprocess = clip.load(model_name)
# model.eval()

# Tokens in climate we want to avoid
with_tokens_set = set(clip.tokenize("with").numpy()[0])
without_tokens_set = set(clip.tokenize("without").numpy()[0])
and_tokens_set = set(clip.tokenize("and").numpy()[0])




climate_to_tokens = {}
with open("../climatetruedict.csv", encoding="utf-8",newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader) # skip header
    for row in reader:
        climate_text = row[1]
        climate_tokens_set = set(clip.tokenize(climate_text).numpy()[0])
        climate_tokens_set = climate_tokens_set - with_tokens_set - without_tokens_set - and_tokens_set
        climate_to_tokens[climate_text] = climate_tokens_set


caption_files = [(i,f"F:cah400M\cah400M{i+1}.txt") for i in range(12)]
# caption_file = "F:\cah400M.txt" # r"/home/data_shares/mapillary/cah400M.txt"
length = 407314954 # length of cah400M.txt file

# label_count = {label:0 for label in climate_to_tokens.keys()} 
def f(x):
    label_count = {label:0 for label in climate_to_tokens.keys()} 

    caption_file = x[1]
    idx = x[0]
    with open(caption_file,encoding="utf-8") as capfile:
        length = len(list(capfile))
    with open(caption_file,encoding="utf-8") as capfile:
        for _ in trange(length):
            caption = capfile.readline().lower()
            try:
                # Due to context length issues some of the captions will be skipped
                caption_tokens_set = set(clip.tokenize(caption).numpy()[0])
            except:
                continue
            for key in climate_to_tokens.keys():
                climate_tokens = climate_to_tokens[key]
                if climate_tokens.issubset(caption_tokens_set):
                    label_count[key] += 1
    with open(f"../label_counts/climate_tokens_labelcount{idx}.json", 'w',encoding="utf-8") as handle:
        json.dump(label_count, handle, ensure_ascii=False,indent=4) 

# inputfile = sys.argv[1]
# with open(f"../label_counts/climate_tokens_labelcount.json", 'w', encoding="utf-8") as handle:
#     json.dump(label_count, handle, ensure_ascii=False, indent=4)

def main():
    with Pool(12) as p:
        p.map(f,caption_files)


if __name__ == "__main__":
    main()