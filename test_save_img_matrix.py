import save_img2matrix

path = "LC08_L2SP_008056_20230502_20230509_02_T1.tar"

img_obj = save_img2matrix.ImgPrepare(file_name=path)

resume, hist_data, deforestation = img_obj.prepare()

print(resume)
