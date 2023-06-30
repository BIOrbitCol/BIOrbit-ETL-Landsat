import os
import uvicorn
import psycopg2
import numpy as np
import save_img2matrix
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Header, HTTPException

HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD_DB = os.getenv("PASSWORD_DB")

app = FastAPI()
TK_ENDPOINT_KEY = os.environ["TOKEN"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/save_data/", status_code=201)
async def download_tk_data(path: str, token: str = Header(...)):

    img_obj = save_img2matrix.ImgPrepare(file_name=path)
    resume, hist_data, deforestation = img_obj.prepare()

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

    json_compatible_data = jsonable_encoder(resume)

    return JSONResponse(content=json_compatible_data)

