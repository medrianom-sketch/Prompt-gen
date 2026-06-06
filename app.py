import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# 1. Configuration
st.set_page_config(page_title="Roseey Personalized Generator", layout="wide")
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)

st.title("📸 Roseey Personalized Generator")

# 2. Sidebar with Full Options and Dynamic 'Custom' Inputs
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("🎥 Media & Platform", expanded=True):
        platform = st.selectbox("PLATFORM", ["Midjourney", "Flux", "Gemini", "YouTube AI", "Meta AI", "Grok", "Veo", "Kling", "Hailuo", "Other"])
        gen_type = st.selectbox("GENERATE", ["Photo Prompt", "Video Prompt", "Thumbnail Prompt", "Everything"])
        voiceover = st.selectbox("VOICEOVER", ["Native Filipina Speaker", "English Speaker", "No Voiceover", "Custom Language"])
        if voiceover == "Custom Language":
            custom_lang = st.text_input("Specify custom language")

    with st.expander("📦 Product & Shot"):
        prod_list = ["Makeup", "Skincare", "Clothing", "Footwear", "Kitchenware", "Home Product", "Toy", "School Supply", "Electronics", "Other"]
        product = st.selectbox("PRODUCT", prod_list)
        if product == "Other":
            product = st.text_input("Describe Product")
        shot_type = st.selectbox("SHOT TYPE", ["Product Close-up", "Handheld", "Mirror Selfie", "Mirror Video", "Lifestyle", "Full Body", "Half Body", "Feet Focus", "Hand Focus"])

    with st.expander("🏠 Environment & Lighting"):
        bg_list = ["Home", "Bedroom", "Living Room", "Kitchen", "Bathroom", "Vanity", "Laundry Area", "Cafe", "Street", "Garden", "Beach", "Pool", "Front Yard", "Studio", "Custom"]
        background = st.selectbox("BACKGROUND", bg_list)
        if background == "Custom":
            background = st.text_input("Describe custom background")
        lighting = st.selectbox("LIGHTING", ["Natural", "Bright Commercial", "Soft Studio", "Luxury", "Moody"])

    with st.expander("🧍 Model & Style"):
        model_type = st.selectbox("MODEL", ["None", "Hand Only", "Feet Only", "Half Body", "Full Body", "Walking", "Sitting"])
        style = st.selectbox("STYLE", ["UGC", "Product Showcase", "Modeling", "Lifestyle", "Problem-Solution", "Review"])

    with st.expander("📋 Rules & Details"):
        rules = st.multiselect("RULES", ["Design Lock", "Face Lock", "No Face", "No Script", "With Script"])
        extra = st.text_area("EXTRA DETAILS")

# 3. Mobile-Optimized File Upload
# accept_multiple_files=True is kept here; if it fails on your specific Android device, 
# change to False to force a single-image workflow.
uploaded_files = st.file_uploader("Upload Reference Photos", type=['jpg', 'png'], accept_multiple_files=True)

if 'engineered_prompt' not in st.session_state:
    st.session_state['engineered_prompt'] = ""

# 4. Step 1: Prompt Generation
if uploaded_files and st.button("🚀 Step 1: Generate Prompt"):
    with st.spinner("Engineering prompt..."):
        image_list = [Image.open(f) for f in uploaded_files]
        prompt_text = (f"Create a professional {gen_type} for {platform}. "
                       f"Product: {product}. Shot: {shot_type}. Background: {background}. "
                       f"Lighting: {lighting}. Style: {style}. Rules: {', '.join(rules)}. {extra}")
        
        response = client.models.generate_content(
            model="gemini-3.5-flash", 
            contents=[prompt_text] + image_list
        )
        st.session_state['engineered_prompt'] = response.text
        st.success("Prompt engineered!")

# 5. Step 2: Image Generation
if st.session_state['engineered_prompt']:
    st.subheader("Final Prompt Review")
    final_prompt = st.text_area("Edit if needed:", st.session_state['engineered_prompt'], height=150)
    
    if st.button("🎨 Step 2: Create Image"):
        with st.spinner("Generating..."):
            try:
                img_response = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=final_prompt,
                    config=types.GenerateImagesConfig(number_of_images=1)
                )
                for gen_img in img_response.generated_images:
                    img_bytes = gen_img.image.image_bytes
                    st.image(Image.open(io.BytesIO(img_bytes)), use_container_width=True)
                    st.download_button("📥 Download", img_bytes, "roseey_result.png", "image/png")
            except Exception as e:
                st.error(f"Generation Error: {e}")
