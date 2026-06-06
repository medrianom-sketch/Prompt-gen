import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# 1. Configuration
st.set_page_config(page_title="Roseey Generator", layout="centered")
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)

st.title("📸 Roseey Personalized Generator")

# 2. Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    with st.expander("🎥 Media & Platform", expanded=True):
        platform = st.selectbox("PLATFORM", ["Midjourney", "Flux", "Gemini", "YouTube AI"])
        gen_type = st.selectbox("GENERATE", ["Photo Prompt", "Video Prompt", "Thumbnail"])
    with st.expander("📦 Product Details"):
        product = st.selectbox("PRODUCT", ["Makeup", "Skincare", "Clothing", "Other"])
        shot_type = st.selectbox("SHOT TYPE", ["Close-up", "Handheld", "Lifestyle", "Full Body"])
    with st.expander("🏠 Environment"):
        background = st.selectbox("BACKGROUND", ["Home", "Studio", "Vanity", "Custom"])
        lighting = st.selectbox("LIGHTING", ["Natural", "Bright Commercial", "Soft Studio"])
    with st.expander("📋 Rules"):
        rules = st.multiselect("RULES", ["Design Lock", "Face Lock", "No Face"])
        extra = st.text_area("EXTRA DETAILS")

# 3. Mobile-Optimized File Uploader
# Using a simple single-upload approach is most reliable for mobile
uploaded_file = st.file_uploader("Upload reference photo", type=['jpg', 'png'])

if 'engineered_prompt' not in st.session_state:
    st.session_state['engineered_prompt'] = ""

# 4. Step 1: Prompt Generation
if uploaded_file and st.button("🚀 Step 1: Generate Prompt"):
    with st.spinner("Analyzing..."):
        image = Image.open(uploaded_file)
        prompt_instructions = f"Create a professional {gen_type} for {platform}. Product: {product}. Rules: {', '.join(rules)}. {extra}"
        
        # FIX: Using 'gemini-3.5-flash' (current stable model)
        response = client.models.generate_content(
            model="gemini-3.5-flash", 
            contents=[prompt_instructions, image]
        )
        st.session_state['engineered_prompt'] = response.text
        st.success("Prompt generated!")

# 5. Step 2: Image Generation
if st.session_state['engineered_prompt']:
    st.subheader("Engineered Prompt")
    final_prompt = st.text_area("Edit Prompt:", st.session_state['engineered_prompt'], height=150)
    
    if st.button("🎨 Step 2: Create Image"):
        with st.spinner("Creating image..."):
            try:
                # FIX: Using 'imagen-3.0-generate-002' (current stable image model)
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
                st.error(f"Image generation failed: {e}")
