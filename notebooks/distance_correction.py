import csv
import pickle
import json
import geopy.distance

with open('../../non_repo_data/file_addresses.json') as json_file:
    data = json.load(json_file)
with open("../../non_repo_data/train.json") as file:
    metadata = json.load(file)
with open('../../non_repo_data/country_to_region.json') as json_file:
    country_to_region = json.load(json_file)
    
for file in list(data.keys()):
    if data[file] == "Error":
        data.pop(file)

CSRF = dict()

for file in data.keys():

    # if file not in all_files:
    #     print(file)
    #     print(data[file])
    #     break
    country = data[file]["country"]
    
    # Use country_to_region dict to check type of region
    state = country_to_region[country]
    # Set the actual region/state e.g "state" for U.S turns to Arizona
    if state in data[file].keys():
        state = data[file][state]
    else:
        state = None
        
    # if road exists in file data save to road
    road = None
    if "road" in data[file].keys():
        road = data[file]["road"]
    
    if road == None and state == None: # Case1
        CSRF.setdefault(country,{"no_road_state":[]})
        CSRF[country]["no_road_state"].append(file)
        
    elif road == None: # Case2
        CSRF.setdefault(country,{"no_road_state":[]})
        CSRF[country].setdefault(state,{"no_road":[]})
        CSRF[country][state]["no_road"].append(file)
        
    elif state == None: # Case4
        CSRF.setdefault(country,{"no_road_state":[]})
        CSRF[country].setdefault(road,{"no_state":[]})
        CSRF[country][road]["no_state"].append(file)
        
    elif state != None and road != None: # Case3
        CSRF.setdefault(country,{"no_road_state":[]})
        CSRF[country].setdefault(state,{"no_road":[]})
        CSRF[country][state].setdefault(road,[])
        CSRF[country][state][road].append(file)
        

file_groups = []
for country in CSRF.keys():
    file_groups.append(CSRF[country]["no_road_state"])
    for state_road in CSRF[country].keys():
        if type(CSRF[country][state_road]) == dict:
            for finalkey in CSRF[country][state_road].keys():
                file_groups.append(CSRF[country][state_road][finalkey])              
accept_list = []
unaccept_list = []

for group in file_groups:
    accept_one = False
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
            elif file2 in unaccept_list or file in unaccept_list:
                pass
            elif geopy.distance.geodesic(coord1,coord2).km < 1:
                unaccept_list.append(file2)
            else:
                if file not in accept_list:
                    accept_list.append(file)
                    
with open(f"accept_list.pickle", 'wb') as handle:
    pickle.dump(accept_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
