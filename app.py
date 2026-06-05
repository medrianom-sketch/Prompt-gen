import streamlit as st
import google.generativeai as genai
from PIL import Image

# Setup API
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.5-flash')

st.title("📸 AI Vision Prompt Generator")

# Sidebar - Full list of categories
st.sidebar.header("Configure Prompt")

platform = st.sidebar.selectbox("📸 PLATFORM", ["ChatGPT Images", "Grok", "Gemini", "Midjourney", "Flux", "Veo", "Kling", "Hailuo", "Meta AI Video", "YouTube AI"])
gen_type = st.sidebar.selectbox("🎯 GENERATE", ["Photo Prompt", "Video Prompt", "Thumbnail Prompt", "Everything"])
product = st.sidebar.selectbox("📦 PRODUCT", ["Makeup", "Skincare", "Clothing", "Footwear", "Kitchenware", "Home Product", "Toy", "School Supply", "Electronics", "Other"])
shot_type = st.sidebar.selectbox("📷 SHOT TYPE", ["Product Close-up", "Handheld", "Mirror Selfie", "Mirror Video", "Lifestyle", "Full Body", "Half Body", "Feet Focus", "Hand Focus"])
background = st.sidebar.selectbox("🏠 BACKGROUND", ["Home", "Bedroom", "Living Room", "Kitchen", "Bathroom", "Vanity", "Laundry Area", "Cafe", "Street", "Garden", "Beach", "Pool", "Front Yard", "Studio", "Custom"])
lighting = st.sidebar.selectbox("☀️ LIGHTING", ["Natural", "Bright Commercial", "Soft Studio", "Luxury", "Moody"])
model_type = st.sidebar.selectbox("🧍 MODEL", ["None", "Hand Only", "Feet Only", "Half Body", "Full Body", "Walking", "Sitting"])
style = st.sidebar.selectbox("✨ STYLE", ["UGC", "Product Showcase", "Modeling", "Lifestyle", "Problem-Solution", "Review"])
rules = st.sidebar.multiselect("📋 RULES", ["Design Lock", "Face Lock", "No Face", "No Script", "With Script"])
extra = st.sidebar.text_area("📝 EXTRA DETAILS")

# Input Method
input_method = st.radio("Choose Input Method", ["Upload File", "Take Photo with Camera"])
if input_method == "Upload File":
    uploaded_file = st.file_uploader("Upload reference photo", type=['jpg', 'png'])
else:
    uploaded_file = st.camera_input("Take a photo")

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Reference Image", use_column_width=True)
    
    if st.button("GENERATE PROMPT"):
        rules_text = ', '.join(rules)
        prompt_instructions = (
            f"Analyze this image and create a professional prompt for {platform}. "
            f"Generate: {gen_type} | Product: {product} | Shot: {shot_type} | "
            f"Background: {background} | Lighting: {lighting} | Model: {model_type} | "
            f"Style: {style} | Rules: {rules_text} | Extra: {extra}"
        )
        
        response = model.generate_content([prompt_instructions, image])
        st.subheader("Generated Prompt:")
        st.code(response.text, language='text')
elif not api_key:
    st.error("API Key not found. Please add it to your app's Settings > Secrets.")
