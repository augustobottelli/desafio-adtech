from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from models import CoordsParams
from libcrop import Model

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict")
async def get_predictions(coordinates_params: List[CoordsParams]):
    prediction = make_prediction(**coordinates_params)
    return prediction
