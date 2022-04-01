import csv
import pickle
import json
import sys
from img2vec_pytorch import Img2Vec
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
    
with open("../inputdata/file_groups.pickle", 'rb') as handle:
    file_groups = pickle.load(handle)

stride =int(sys.argv[1])
start = int(sys.argv[2])
def splitter(lst,stride,start):
    return lst[start::stride]
img2vec = Img2Vec(cuda=True)
file_src = "/home/data_shares/mapillary/train/"              
accept_list = []
unaccept_set = set()
file_groups = splitter(file_groups,stride,start)
for group in file_groups:
    accept_one = False
    if group == []:
        continue
    for file in group:
        if accept_one == False:
                accept_one = True
                accept_list.append(file)
        for file2 in group:
            file = file_src + file + ".jpg"
            file2 = file_src + file2 + ".jpg"
            if file == file2:
                continue
            elif file2 in unaccept_set or file in unaccept_set:
                continue
            try:
                img1 = Image.open(file).convert('RGB')
                img2 = Image.open(file2).convert('RGB')
                vec1 = img2vec.get_vec(img1, tensor=True).reshape(1, -1)
                vec2 = img2vec.get_vec(img2, tensor=True).reshape(1, -1)
                cos_sim = cosine_similarity(vec1, vec2)[0][0]
            except:
                print("error with file or file2 image opening")
                continue
            
            if cos_sim > 0.9:
                unaccept_set.add(file2)
            else:
                if file not in accept_list:
                    accept_list.append(file)
                    
with open(f"accept_list{start}.pickle", 'wb') as handle:
    pickle.dump(accept_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
with open(f"unaccept_set{start}.pickle", 'wb') as handle:
    pickle.dump(unaccept_set, handle, protocol=pickle.HIGHEST_PROTOCOL)
