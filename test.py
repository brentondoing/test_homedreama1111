# This file is used to verify your http server acts as expected
# Run it with `python3 test.py``

import requests
import base64
from io import BytesIO
from PIL import Image

# URL of the image to be added to the JSON object
# image_url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image_url = "https://i.imgur.com/HiTEFB8.jpeg"

# Download the image from the URL
response = requests.get(image_url)

# Encode the image data as base64
base64_image = base64.b64encode(response.content).decode("utf-8")

model_inputs = {
  "endpoint": "img2img",
  "params": {
    "prompt": "remodeled kitchen",
    "negative_prompt": "cartoonish, low quality",
    "steps": 25,
    "sampler_name": "Euler a",
    "cfg_scale": 7.5,
    # "seed": 42,
    "batch_size": 1,
    "n_iter": 1,
    "width": 512,
    "height": 512,
    "tiling": False,
    "init_images": [base64_image],
    # "mask": [base64_mask]
  }
}

# model_inputs = {'prompt': 'realistic field of grass'}

res = requests.post('http://localhost:8000/', json = model_inputs)

print(res.json().keys())

image_byte_string = res.json()["images"][0]

image_encoded = image_byte_string.encode('utf-8')
image_bytes = BytesIO(base64.b64decode(image_encoded))
image = Image.open(image_bytes)
image.save("output.jpg")