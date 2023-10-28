# Product Image Background Removal using DIS

This project uses the DIS (Deep Image Segmentation) model to remove the background of product images. The background is then replaced with depth information from SDXL 1.0 based controlnet depth.

# Requirements

PyTorch Version: 2.1.0 (compiled with CUDA 11.8)
GPU: Tesla T4 (with 15,360 MiB of memory available)

# Installation
To install the required packages, first make sure you have Python and pip installed. Then, run the following command:



pip install -r requirements.txt
The requirements.txt file includes the following packages:


# Usage
Start the FastAPI server:
uvicorn main:app --reload

This command will launch the FastAPI server, and you can access the API at http://127.0.0.1:8000/docs.

Use the API endpoints as described in main.py to send your product image and the desired prompt. The API will process the image, remove the background, and replace it with  information. The resulting image will be sent back as a response.
