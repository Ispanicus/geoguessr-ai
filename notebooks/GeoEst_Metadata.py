"""Loads all geoestimation predictions of Mapillary dataset and uses geopy to fetch address"""
import json
import csv
from unittest import result
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
idx = 0 
result_metadata = {}
loaded=False
progressfilename = f"../progress/GeoEst_Metadata_progress.out"


with open("../../GeoEstimation/geo_alltrain_results.csv", encoding="utf-8",newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        idx +=1
        row = row[0].split(',')
        if row[0]=="img_id":
            print(row)
            continue
        filename = row[0]
        grade = row[1]
        lat = row[3]
        lon = row[4]
        result_metadata.setdefault(filename,{"coarse":dict(),
                                   "middle":dict(),
                                   "fine":dict(),
                                   "hierarchy":dict()})
        result_metadata[filename][grade]["lat"] = lat
        result_metadata[filename][grade]["lon"] = lon
            
        try: 
            location = geolocator.reverse((lat, lon),language='en')
            address = location.raw['address']
            result_metadata[filename][grade]["address"] = address
        except:
            result_metadata[filename][grade]["address"] = "Error"
        
        if idx % 10000:
            with open(progressfilename, "w") as progressfile:
                progressfile.write(f"Progress: {100*idx/2968389:.2f}%")
        
        
with open("../../geo_est_metadata.json", 'w',encoding="utf-8") as handle:
    json.dump(result_metadata, handle, ensure_ascii=False,indent=4) 