from Utils import LAION_label_count
import os
import pickle

for file in os.listdir("../inputdata/"):
    if file[-4:] != ".csv":
        continue
    print(f"Processing {file}")
    label_count = LAION_label_count(file)
    with open(f"../label_counts/{file[:-4]}_labelcount.pickle", 'wb') as handle:
        pickle.dump(label_count, handle, protocol=pickle.HIGHEST_PROTOCOL)