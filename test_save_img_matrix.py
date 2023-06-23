import os
import landsat
import psycopg2
import numpy as np
import save_img2matrix
from landsat import LandsatAPI
import matplotlib.pyplot as plt

HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD_DB = os.getenv("PASSWORD_DB")

# # Site's coord (EPSG:4326)
# latitude = "5.48333"
# longitude = "-75.0667"
#
# # USGS website
# username = os.getenv("USERNAME")
# password = os.getenv("PASSWORD")
#
# # chromedriver path
# chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
# geojson_path = os.getenv("GEOJSON_PATH")
#
# # Download folder
# downloads_dir = os.getenv("DOWNLOADS_DIR")
#
# footprint = landsat.get_footprint(latitude, longitude, geojson_path)
#
# # Download imagen Landsat 8
# api = LandsatAPI(username, password, chromedriver_path, downloads_dir)
# tar_list = api.query(chromedriver_path, downloads_dir, footprint, 15)

path = "LC08_L2SP_008056_20230502_20230509_02_T1.tar"
# path = tar_list[0]

img_obj = save_img2matrix.ImgPrepare(file_name=path)

resume, hist_data, deforestation = img_obj.prepare()

print(resume)

plt.hist(hist_data)
plt.show()

img_to_save = img_obj.rgb()

np.savez_compressed(f"ndvi_folder/def_{path.split('.')[0]}.npz", a=deforestation)
np.savez_compressed(f"ndvi_folder/img_{path.split('.')[0]}.npz", a=img_to_save)

conn = psycopg2.connect(host=HOST,
                        database=DATABASE,
                        user=USER,
                        password=PASSWORD_DB)

test_name = "test_name"
test = "test"

insert_db = f"INSERT INTO public.ndvi_biorbit" \
            f'("name", deforestation, mean, "date", percentage, total_px, "comment")' \
            f"VALUES('{path}', {resume.get('deforestation')}, {resume.get('mean')}, CURRENT_DATE, {resume.get('percentage')}, {resume.get('total_px')}, '{test}');"

cur = conn.cursor()

cur.execute(insert_db)
conn.commit()
cur.close()

print(insert_db)


