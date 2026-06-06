import streamlit as st
import google.generativeai as genai
from PIL import Image

# Setup API
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.5-flash')

st.title("📸 AI Vision Prompt Generator")

# Sidebar - Full list
with st.sidebar:
    st.header("Configure Prompt")
    platform = st.selectbox("📸 PLATFORM", ["ChatGPT Images", "Grok", "Gemini", "Midjourney", "Flux", "Veo", "Kling", "Hailuo", "Meta AI Video", "YouTube AI"])
    gen_type = st.selectbox("🎯 GENERATE", ["Photo Prompt", "Video Prompt", "Thumbnail Prompt", "Everything"])
    
    # New options: voiceover and custom language
    voiceover = st.selectbox("🎙️ VOICEOVER", ["Native Filipina Speaker", "English Speaker", "No Voiceover", "Custom Language"])
    if voiceover == "Custom Language":
        custom_language = st.text_input("Specify custom language")
    
    product = st.selectbox("📦 PRODUCT", ["Makeup", "Skincare", "Clothing", "Footwear", "Kitchenware", "Home Product", "Toy", "School Supply", "Electronics", "Other"])
    shot_type = st.selectbox("📷 SHOT TYPE", ["Product Close-up", "Handheld", "Mirror Selfie", "Mirror Video", "Lifestyle", "Full Body", "Half Body", "Feet Focus", "Hand Focus"])
    
    # Background logic
    background = st.selectbox("🏠 BACKGROUND", ["Home", "Bedroom", "Living Room", "Kitchen", "Bathroom", "Vanity", "Laundry Area", "Cafe", "Street", "Garden", "Beach", "Pool", "Front Yard", "Studio", "Custom"])
    custom_bg = st.text_input("If 'Custom', describe it (e.g., white wall aesthetic kitchen)")
    
    lighting = st.selectbox("☀️ LIGHTING", ["Natural", "Bright Commercial", "Soft Studio", "Luxury", "Moody"])
    model_type = st.selectbox("🧍 MODEL", ["None", "Hand Only", "Feet Only", "Half Body", "Full Body", "Walking", "Sitting"])
    style = st.selectbox("✨ STYLE", ["UGC", "Product Showcase", "Modeling", "Lifestyle", "Problem-Solution", "Review"])
    rules = st.multiselect("📋 RULES", ["Design Lock", "Face Lock", "No Face", "No Script", "With Script"])
    extra = st.text_area("📝 EXTRA DETAILS")

# Mobile-Friendly Input
tab1, tab2 = st.tabs(["📸 Use Camera", "📁 Upload from Gallery"])
uploaded_file = None
with tab1: camera_file = st.camera_input("Take a photo"); uploaded_file = camera_file
with tab2: file_file = st.file_uploader("Choose a photo", type=['jpg', 'png']); uploaded_file = file_file

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Reference Image", use_column_width=True)
    
    if st.button("GENERATE PROMPT"):
        with st.spinner("Analyzing..."):
            final_bg = custom_bg if background == "Custom" else background
            rules_text = ', '.join(rules)
            
            # Constructing voiceover part of prompt
            voiceover_prompt = f"Voiceover: {voiceover}"
            if voiceover == "Custom Language":
                voiceover_prompt += f" ({custom_language})"

            # The "Magic" layer: Force accuracy and avoid AI errors
            prompt_instructions = (
                f"Analyze this image and create a professional prompt for {platform}. "
                f"Generate: {gen_type} | {voiceover_prompt} | Product: {product} | Shot: {shot_type} | Background: {final_bg} | "
                f"Lighting: {lighting} | Model: {model_type} | Style: {style} | Rules: {rules_text}. "
                f"TECHNICAL QUALITY & ACCURACY RULES: 1. Ensure absolute anatomical correctness (no extra fingers, no fused limbs, realistic hand/feet structures). 2. Maintain structural integrity of the product (no distortion, no melting shapes). 3. Use cinematic, hyper-realistic, 8k resolution standards with sharp focus and professional lighting. 4. {extra}"
            )
            
            response = model.generate_content([prompt_instructions, image])
            st.subheader("Generated Prompt:")
            st.code(response.text, language='text')
