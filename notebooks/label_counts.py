from Utils import LAION_label_count
import os
import json
import sys

if len(sys.argv) > 1:
    target_file = sys.argv[1]
    label_count = LAION_label_count(target_file)
    with open(f"../label_counts/{file[:-4]}_labelcount.json", 'w', encoding="utf-8") as handle:
        json.dump(label_count, handle, ensure_ascii=False, indent=4)
    
else:
   
    for file in os.listdir("../inputdata/"):
        if file[-4:] != ".csv":
            continue
        print(f"Processing {file}")
        label_count = LAION_label_count(file)
        with open(f"../label_counts/{file[:-4]}_labelcount.json", 'w', encoding="utf-8") as handle:
            json.dump(label_count, handle, ensure_ascii=False, indent=4)
