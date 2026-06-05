import streamlit as st
import google.generativeai as genai
from PIL import Image

# Setup API
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.5-flash')

st.title("📸 AI Vision Prompt")

# Sidebar - All categories restored
with st.sidebar:
    st.header("Configure Prompt")
    platform = st.selectbox("📸 PLATFORM", ["ChatGPT Images", "Grok", "Gemini", "Midjourney", "Flux", "Veo", "Kling", "Hailuo", "Meta AI Video", "YouTube AI"])
    gen_type = st.selectbox("🎯 GENERATE", ["Photo Prompt", "Video Prompt", "Thumbnail Prompt", "Everything"])
    product = st.selectbox("📦 PRODUCT", ["Makeup", "Skincare", "Clothing", "Footwear", "Kitchenware", "Home Product", "Toy", "School Supply", "Electronics", "Other"])
    shot_type = st.selectbox("📷 SHOT TYPE", ["Product Close-up", "Handheld", "Mirror Selfie", "Mirror Video", "Lifestyle", "Full Body", "Half Body", "Feet Focus", "Hand Focus"])
    style = st.selectbox("✨ STYLE", ["UGC", "Product Showcase", "Modeling", "Lifestyle", "Problem-Solution", "Review"])
    extra = st.text_area("📝 EXTRA DETAILS")

# Mobile-Friendly Tabs
tab1, tab2 = st.tabs(["📸 Use Camera", "📁 Upload from Gallery"])

uploaded_file = None

with tab1:
    camera_file = st.camera_input("Take a photo")
    if camera_file:
        uploaded_file = camera_file

with tab2:
    file_file = st.file_uploader("Choose a photo", type=['jpg', 'png'])
    if file_file:
        uploaded_file = file_file

# Processing
if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Reference Image", use_column_width=True)
    
    if st.button("GENERATE PROMPT"):
        with st.spinner("Analyzing..."):
            prompt_instructions = (
                f"Analyze this image and create a professional prompt for {platform}. "
                f"Generate: {gen_type} | Product: {product} | Shot: {shot_type} | "
                f"Style: {style} | Extra: {extra}"
            )
            response = model.generate_content([prompt_instructions, image])
            st.subheader("Your Prompt:")
            st.code(response.text, language='text')
elif not api_key:
    st.error("API Key not found in Secrets.")
