import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import base64
import requests

st.set_page_config(page_title="Drawing with Gemini", layout="centered")
st.title("🎨 Drawing Pad with Gemini API")

# Sidebar Settings
st.sidebar.header("Canvas Options")
stroke_width = st.sidebar.slider("Stroke Width", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke Color", "#000000")
bg_color = st.sidebar.color_picker("Background Color", "#ffffff")
drawing_mode = st.sidebar.selectbox("Drawing Mode", ("freedraw", "line", "rect", "circle", "transform"))

# Drawing Canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=400,
    width=600,
    drawing_mode=drawing_mode,
    update_streamlit=True,
    key="canvas"
)

# Handle drawing image
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data, caption="Your Drawing", use_column_width=True)

    # Convert canvas to PIL image
    image = Image.fromarray(canvas_result.image_data.astype("uint8"), mode="RGBA")

    # Download
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button("📥 Download Drawing", data=byte_im, file_name="drawing.png", mime="image/png")

    # Gemini Integration
    st.subheader("🔗 Analyze Drawing with Gemini")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    prompt = st.text_area("Prompt for Gemini", "Describe this image...")

    if st.button("Send to Gemini"):
        if not api_key:
            st.warning("Please enter your Gemini API key.")
        else:
            # Convert image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            # API Call
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={api_key}"

            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": "image/png",
                                    "data": img_base64
                                }
                            }
                        ]
                    }
                ]
            }

            response = requests.post(endpoint, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                reply = result["candidates"][0]["content"]["parts"][0]["text"]
                st.success("Gemini Response:")
                st.write(reply)
            else:
                st.error("Failed to get response from Gemini API")
                st.json(response.json())