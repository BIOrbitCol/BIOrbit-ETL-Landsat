import numpy as np
import save_img2matrix
import matplotlib.pyplot as plt

path = "LC08_L2SP_008056_20230502_20230509_02_T1.tar"

img_obj = save_img2matrix.ImgPrepare(file_name=path)

resume, hist_data, deforestation = img_obj.prepare()

print(resume)

plt.hist(hist_data)
plt.show()

img_to_save = img_obj.rgb()

np.savez_compressed(f"ndvi_folder/def_{path.split('.')[0]}.npz", a=deforestation)
np.savez_compressed(f"ndvi_folder/img_{path.split('.')[0]}.npz", a=img_to_save)


