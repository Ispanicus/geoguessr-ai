import pickle
import json
import sys
import os
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
idx = jdx = 0 
file_metadata = {}
try:
    with open(sys.argv[1]) as file:
        metadata = json.load(file)
except:
    print("Failed to open metadata file, make sure to pass as first argument. Current first argument is: ", )
    try:
        print(sys.argv[1])
    except:
        print("Failed to get first argument")
        
try:
    print("making directory country_dataset")
    os.mkdir("country_datatest")
except:
    print("country_dataset directory already exists")
for file in metadata.keys():
    idx += 1
    if f"country_data{jdx}.pickle" in os.listdir(country_data):
        print(f"found country_data{jdx}, so continuing")
        if idx == 10:
            idx = 0
            jdx += 1
        continue
    try: 
        lat = metadata[file]["lat"]
        long = metadata[file]["lon"]
        location = geolocator.reverse((lat, long),language='en,*-Latn')
        address = location.raw['address']
    #     country = address.get('country', '')
        file_metadata[file] = address
    except:
        file_metadata[file] = "Error"
    
    if idx == 10:
        idx = 0
        
        with open(f"country_datatest/country_datatest{jdx}.pickle", 'wb') as handle:
            pickle.dump(file_metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)
        jdx += 1
    if jdx == 3:
        break
with open("country_datatest/country_datatest_final.pickle", 'wb') as handle:
    pickle.dump(file_metadata, handle, protocol=pickle.HIGHEST_PROTOCOL) 