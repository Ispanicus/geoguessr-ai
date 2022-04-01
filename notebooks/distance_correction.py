import csv
import pickle
import json
import geopy.distance
import sys
    
with open("../file_groups.pickle", 'rb') as handle:
    file_groups = pickle.load(handle)
    
stride = sys.argv[1]
start = sys.argv[2]
def splitter(lst,stride,start):
    return lst[start::stride]

#              
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
            try:
                coord1 = (metadata[file]['lat'],metadata[file]['lon'])
                coord2 = (metadata[file2]['lat'],metadata[file2]['lon'])
            except:
                print("error with file or file2 metadata")
            if file == file2:
                pass
            elif file2 in unaccept_set or file in unaccept_set:
                pass
            elif geopy.distance.great_circle(coord1,coord2).km < 1:
                unaccept_set.add(file2)
            else:
                if file not in accept_list:
                    accept_list.append(file)
                    
with open(f"accept_list{start}.pickle", 'wb') as handle:
    pickle.dump(accept_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
with open(f"unaccept_set{start}.pickle", 'wb') as handle:
    pickle.dump(unaccept_set, handle, protocol=pickle.HIGHEST_PROTOCOL)
