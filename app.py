import streamlit as st
from PIL import Image
import cv2
import numpy as np
import subprocess
import os
import glob

def file_upload():
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg'])
    uploaded_file_name = ""
    if uploaded_file is not None:
        uploaded_file_name = uploaded_file.name
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        st.image(img_array, caption='Uploaded Image', use_column_width=True)
        return img_array, uploaded_file_name


def main():
    RUNS_PATH = 'runs/detect'

    st.title('Image Upload')
    image_upload = file_upload()
    if image_upload is not None:
        image, file_name = image_upload
    else:
        image = file_name = None

    if image is not None:
        command = ["python", "detect.py", "--weights", "best.pt", "--conf", "0.5", "--img-size", "800", "--source", 
           file_name, "--view-img", "--no-trace", "--project", "runs/detect", "--name", "run"]
        process = subprocess.Popen(command, shell=True)
        process.wait()

        files = glob.glob(RUNS_PATH + '/*')
        latest_file = max(files, key=os.path.getctime)
        print(latest_file)
        image = Image.open(os.path.join(latest_file, file_name))
        img_array = np.array(image)
        st.image(img_array, caption='Predictions on image', use_column_width=True)

if __name__ == '__main__':
    main()