import streamlit as st
import google.generativeai as genai
from PIL import Image

# This will automatically pull the key you saved in Settings > Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")
# Diagnostic: Print available models
st.write("--- Available Models ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        st.write(m.name)
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📸 AI Vision Prompt Generator")
uploaded_file = st.file_uploader("Upload reference photo", type=['jpg', 'png'])

# Sidebar - All your original options
st.sidebar.header("Configure Prompt")
platform = st.sidebar.selectbox("📸 PLATFORM", ["ChatGPT", "Grok", "Gemini", "Midjourney", "Flux", "Veo", "Kling", "Hailuo", "Meta AI Video", "YouTube"])
gen_type = st.sidebar.selectbox("🎯 GENERATE", ["Photo Prompt", "Video Prompt", "Thumbnail Prompt"])
product = st.sidebar.text_input("📦 PRODUCT")
shot_type = st.sidebar.selectbox("📷 SHOT TYPE", ["Product Close-up", "Handheld", "Lifestyle"])
style = st.sidebar.selectbox("✨ STYLE", ["UGC", "Cinematic", "Minimalist"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("GENERATE PROMPT"):
        prompt_instructions = f"Analyze this image and create a prompt for {platform} for a {gen_type} of {product}. Use {shot_type} shot in {style} style."
        response = model.generate_content([prompt_instructions, image])
        st.subheader("Generated Prompt:")
        st.write(response.text)
elif not api_key:
    st.error("API Key not found. Please add it to your app's Settings > Secrets.")
