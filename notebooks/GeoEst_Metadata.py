"""Loads all geoestimation predictions of Mapillary dataset and uses geopy to fetch address"""
import json
import csv
from geopy.geocoders import Nominatim
from multiprocessing import Pool
from tqdm import tqdm
geolocator = Nominatim(user_agent="geoapiExercises")
def chunks(lst, i):
    """Yield successive n-sized chunks from lst."""
    n = round(len(lst)/i)
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

with open("../../GeoEstimation/geo_alltrain_results.csv", encoding="utf-8",newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    list_csv = list(reader)
list_csv.pop(0)

list_of_chunks = chunks(list_csv,72)
list_of_chunks_enum = []
for idx, chunk in enumerate(list_of_chunks):
    list_of_chunks_enum.append((idx,chunk))


def f(x):
    result_metadata = {}
    idx = x[0]
    lst = x[1]
    idx2 = 0
    progressfilename = f"../progress/GeoEst_chunk_{idx2}_prog.out" 
    for row in lst:
        idx2 += 1
        row = row[0].split(',')
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
        
        if idx2 % 1000 == 0:
            with open(progressfilename, 'w') as progressfile:
                progressfile.write(f"Progress: {100*idx2/len(lst):.2f}%")
    
    with open(f"../../geo_metadata_chunks/geo_est_metadata{idx}.json", 'w',encoding="utf-8") as handle:
        json.dump(result_metadata, handle, ensure_ascii=False,indent=4) 

def main():
    with Pool(72) as p:
        p.map(f,list_of_chunks_enum)


if __name__ == "__main__":
    main()