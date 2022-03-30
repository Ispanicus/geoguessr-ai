import matplotlib.pyplot as plt
import sys, os, pickle
from PIL import Image

img_src = "/home/data_shares/mapillary/train/"
img_list = sys.argv[1]
with open(os.path.join("../figureinput",img_list), 'rb') as handle:
    image_list = pickle.load(handle)
    
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(8, 8))
image_gen = iter(image_list)

plt.title(img_list[:-7])
for row in axes:
    for col in row:
        filename = next(image_gen)
        image = Image.open(os.path.join(img_src,filename+".jpg")).convert("RGB")
        col.imshow(image)

plt.tight_layout()
plt.savefig(os.path.join("../figures/", img_list[:-7]+".png"))
