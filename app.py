import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure Gemini
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📸 AI Vision Prompt Generator")

# File uploader
uploaded_file = st.file_uploader("Upload reference photo", type=['jpg', 'png'])

# Sidebar selections
style = st.sidebar.selectbox("✨ STYLE", ["UGC", "Cinematic", "Minimalist"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Analyze & Generate Prompt"):
        prompt_instructions = f"Analyze this image and write a detailed AI generation prompt in {style} style, focusing on lighting, composition, and product details."
        response = model.generate_content([prompt_instructions, image])
        st.subheader("Generated Prompt:")
        st.write(response.text)
