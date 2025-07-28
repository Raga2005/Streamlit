import streamlit as st
import cv2
from PIL import Image
import numpy as np
import google.generativeai as genai

# ----------------------------
# Paste your Gemini API Key 👇
# ----------------------------
GEMINI_API_KEY = "AIzaSyD-Yat3AG1c-JvWlNQoyQcGfXILglNiMD8"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  # or 'gemini-1.5-pro'


st.title("🎯 Face Count Detection with Gemini API")
st.markdown("Capture webcam frame, send to Gemini Vision API, and get number of faces.")

if st.button("📸 Capture Frame & Detect Faces"):
    # Capture one frame from webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        st.error("Failed to capture image from webcam.")
    else:
        # Convert frame (OpenCV BGR → RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_rgb)

        # Display the image
        st.image(img_pil, caption="Captured Frame", use_column_width=True)

        # Send to Gemini
        with st.spinner("Analyzing image with Gemini..."):
            prompt = "Count the number of human faces in this image. Just say the number and optionally describe their expressions."
            response = model.generate_content([prompt, img_pil])

        # Show the result
        st.success("✅ Gemini Response:")
        st.markdown(response.text)