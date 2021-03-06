import pickle
import json
import sys
import os
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
idx = jdx = 0 
file_metadata = {}
loaded=False
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
    os.mkdir("country_data")
except:
    print("country_dataset directory already exists")
for file in metadata.keys():
    
    idx += 1
    if f"country_data{jdx}.pickle" in os.listdir("country_data"):
        if idx == 1000:
            idx = 0
            jdx += 1
        continue
    elif f"country_data{jdx-1}.pickle" in os.listdir("country_data") and not loaded:
        loaded=True
        with open(f"country_data/country_data{jdx-1}.pickle", 'rb') as handle:
            file_metadata=pickle.load(handle)
        
    try: 
        lat = metadata[file]["lat"]
        long = metadata[file]["lon"]
        location = geolocator.reverse((lat, long),language='en')
        address = location.raw['address']
    #     country = address.get('country', '')
        file_metadata[file] = address
    except:
        file_metadata[file] = "Error"
    
    if idx == 1000:
        idx = 0
        with open(f"country_data/country_data{jdx}.pickle", 'wb') as handle:
            pickle.dump(file_metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)
        jdx += 1
with open("country_data/country_data_final.pickle", 'wb') as handle:
    pickle.dump(file_metadata, handle, protocol=pickle.HIGHEST_PROTOCOL) 