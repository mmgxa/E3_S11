import requests
import torch
from io import BytesIO
from typing import Annotated, List, Optional
import base64

import numpy as np

from fastapi import FastAPI, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from PIL import Image
from datasets import load_dataset
from transformers import CLIPProcessor, CLIPModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


@app.post("/clip")
async def find_image(text: str, image: Annotated[bytes, File()]):

    img: Image.Image = Image.open(BytesIO(image))
    # img: Image.Image = Image.open(base64.b64decode(image))
    img = img.convert("RGB")  
    text_list = text.split(",")
    inputs = processor(text=text_list, images=img, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model(**inputs)

    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)[0] 

    ret_img = BytesIO()
    img.save(ret_img, format="jpeg")

    return {text_list[i]: round(probs[i].item()*100,2) for i in range(len(text_list))}

@app.get("/health")
async def health():
    return {"message": "ok"}