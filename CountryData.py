import pickle
import json
import sys
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
for file in tqdm(metadata.keys()):
    idx += 1
    try: 
        lat = metadata[file]["lat"]
        long = metadata[file]["lon"]
        location = geolocator.reverse((lat, long))
        address = location.raw['address']
    #     country = address.get('country', '')
        file_metadata[file] = address
    except:
        file_metadata[file] = "Error"
    
    if idx == 10000:
        idx = 0
        jdx += 1
        with open(f"country_data/country_data{jdx}.pickle", 'wb') as handle:
            pickle.dump(country_guess, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open("country_data/country_data_final.pickle", 'wb') as handle:
    pickle.dump(country_guess, handle, protocol=pickle.HIGHEST_PROTOCOL) 