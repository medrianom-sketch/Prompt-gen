import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# 1. Setup API
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)

st.set_page_config(page_title="Roseey Personalized Generator", layout="centered")
st.title("📸 Roseey Personalized Generator")

# 2. Sidebar Setup
with st.sidebar:
    st.header("Configure Prompt")
    platform = st.selectbox("📸 PLATFORM", ["ChatGPT Images", "Grok", "Gemini", "Midjourney", "Flux", "Veo", "Kling", "Hailuo", "Meta AI Video", "YouTube AI"])
    gen_type = st.selectbox("🎯 GENERATE", ["Photo Prompt", "Video Prompt", "Thumbnail Prompt", "Everything"])
    voiceover = st.selectbox("🎙️ VOICEOVER", ["Native Filipina Speaker", "English Speaker", "No Voiceover", "Custom Language"])
    custom_language = st.text_input("If 'Custom Language', specify here")
    product = st.selectbox("📦 PRODUCT", ["Makeup", "Skincare", "Clothing", "Footwear", "Kitchenware", "Home Product", "Toy", "School Supply", "Electronics", "Other"])
    shot_type = st.selectbox("📷 SHOT TYPE", ["Product Close-up", "Handheld", "Mirror Selfie", "Mirror Video", "Lifestyle", "Full Body", "Half Body", "Feet Focus", "Hand Focus"])
    background = st.selectbox("🏠 BACKGROUND", ["Home", "Bedroom", "Living Room", "Kitchen", "Bathroom", "Vanity", "Laundry Area", "Cafe", "Street", "Garden", "Beach", "Pool", "Front Yard", "Studio", "Custom"])
    custom_bg = st.text_input("Custom background description")
    lighting = st.selectbox("☀️ LIGHTING", ["Natural", "Bright Commercial", "Soft Studio", "Luxury", "Moody"])
    model_type = st.selectbox("🧍 MODEL", ["None", "Hand Only", "Feet Only", "Half Body", "Full Body", "Walking", "Sitting"])
    style = st.selectbox("✨ STYLE", ["UGC", "Product Showcase", "Modeling", "Lifestyle", "Problem-Solution", "Review"])
    rules = st.multiselect("📋 RULES", ["Design Lock", "Face Lock", "No Face", "No Script", "With Script"])
    extra = st.text_area("📝 EXTRA DETAILS")

# 3. Image Upload
uploaded_file = st.file_uploader("Choose a photo", type=['jpg', 'png'])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Reference Image", use_container_width=True)
    
    if st.button("🚀 GENERATE PROMPT & IMAGE"):
        with st.spinner("Processing..."):
            final_bg = custom_bg if background == "Custom" else background
            voice_text = f"{voiceover} ({custom_language})" if voiceover == "Custom Language" else voiceover
            
            prompt_text = (
                f"Create a professional {gen_type} for {platform}. "
                f"Details: Product: {product}, Shot: {shot_type}, BG: {final_bg}, "
                f"Lighting: {lighting}, Style: {style}, Voiceover: {voice_text}. "
                f"Rules: {', '.join(rules)}. Extra: {extra}. "
                f"STRICT RULES: Anatomically perfect, 8k realism, no distortion."
            )
            
            # Text Prompt Generation
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=[prompt_text, image]
            )
            st.subheader("Generated Prompt:")
            st.code(response.text)
            
            # Image Generation
            try:
                img_response = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=response.text,
                    config=types.GenerateImagesConfig(number_of_images=1)
                )
                for gen_img in img_response.generated_images:
                    img_bytes = gen_img.image.image_bytes
                    st.image(Image.open(io.BytesIO(img_bytes)), caption="Generated Result")
                    st.download_button("📥 Download Image", img_bytes, "roseey_result.png", "image/png")
            except Exception as e:
                st.error(f"Image generation failed: {e}")
