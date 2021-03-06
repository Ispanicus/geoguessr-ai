import csv
import pickle
import json
import sys
from img2vec_pytorch import Img2Vec
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

with open("../pickles/file_groups.pickle", 'rb') as handle:
    file_groups = pickle.load(handle)

# stride =int(sys.argv[1])
# start = int(sys.argv[2])
start = "total"
# def splitter(lst,stride,start):
#     return lst[start::stride]
img2vec = Img2Vec(cuda=True)
# file_src = "/home/data_shares/mapillary/train/"
file_src = "F:\Mapillary\\train\\" 
accept_list = []
unaccept_set = set()
# file_groups = splitter(file_groups,stride,start)
for group in tqdm(file_groups):
    accept_one = False
    if group == []:
        continue
        
    image_dic = {}
    vec_dic = {}
    for file in tqdm(group,leave=False):
        file_path = file_src + file + ".jpg"

        img1 = Image.open(file_path).convert('RGB')
        vec1 = img2vec.get_vec(img1, tensor=True).reshape(1, -1)
        image_dic[file] = img1
        vec_dic[file] = vec1
    for file in tqdm(group, leave=False):
        if accept_one == False:
                accept_one = True
                accept_list.append(file)
        img1 = image_dic[file]
        vec1 = vec_dic[file]
        for file2 in group:
            
            if file == file2:
                continue
            elif file2 in unaccept_set or file in unaccept_set:
                continue
            
            img2 = image_dic[file2]
            vec2 = vec_dic[file2]
            cos_sim = cosine_similarity(vec1, vec2)[0][0]
    
            
            if cos_sim > 0.9:
                unaccept_set.add(file2)
            else:
                if file not in accept_list:
                    accept_list.append(file)
                    
with open(f"cossim_accept_list{start}.pickle", 'wb') as handle:
    pickle.dump(accept_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
with open(f"cossim_unaccept_set{start}.pickle", 'wb') as handle:
    pickle.dump(unaccept_set, handle, protocol=pickle.HIGHEST_PROTOCOL)
