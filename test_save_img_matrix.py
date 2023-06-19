import os
import psycopg2
import numpy as np
import save_img2matrix
import matplotlib.pyplot as plt

HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD_DB = os.getenv("PASSWORD_DB")

path = "LC08_L2SP_008056_20230502_20230509_02_T1.tar"

img_obj = save_img2matrix.ImgPrepare(file_name=path)

resume, hist_data, deforestation = img_obj.prepare()

print(resume)

# plt.hist(hist_data)
# plt.show()
#
# img_to_save = img_obj.rgb()
#
# np.savez_compressed(f"ndvi_folder/def_{path.split('.')[0]}.npz", a=deforestation)
# np.savez_compressed(f"ndvi_folder/img_{path.split('.')[0]}.npz", a=img_to_save)

conn = psycopg2.connect(host=HOST,
                        database=DATABASE,
                        user=USER,
                        password=PASSWORD_DB)

test_name = "test_name"
test = "test"

insert_db = f"INSERT INTO public.ndvi_biorbit" \
            f'("name", deforestation, mean, "date", percentage, total_px, "comment")' \
            f"VALUES('{test_name}', {resume.get('deforestation')}, {resume.get('mean')}, CURRENT_DATE, {resume.get('percentage')}, {resume.get('total_px')}, '{test}');"

cur = conn.cursor()

cur.execute(insert_db)
conn.commit()
cur.close()

print(insert_db)


