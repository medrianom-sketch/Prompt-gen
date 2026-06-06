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

# 2. Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    with st.expander("🎥 Media & Platform", expanded=True):
        platform = st.selectbox("PLATFORM", ["Midjourney", "Flux", "Gemini", "Other"])
        gen_type = st.selectbox("GENERATE", ["Photo Prompt", "Video Prompt"])
        voiceover = st.selectbox("VOICEOVER", ["Native Filipina Speaker", "English Speaker", "No Voiceover"])
    
    with st.expander("📦 Product & Shot"):
        product = st.text_input("Product Description", "Skincare bottle")
        shot_type = st.selectbox("SHOT TYPE", ["Product Close-up", "Lifestyle", "Full Body"])

    with st.expander("🏠 Environment & Lighting"):
        background = st.text_input("Background", "Modern minimalist studio")
        lighting = st.selectbox("LIGHTING", ["Natural", "Bright Commercial", "Soft Studio"])

    with st.expander("🧍 Model & Style"):
        style = st.selectbox("STYLE", ["UGC", "Product Showcase", "Lifestyle"])
        rules = st.multiselect("RULES", ["No Face", "With Script"])
        extra = st.text_area("EXTRA DETAILS")

# 3. File Upload
uploaded_file = st.file_uploader("Upload Reference Photo", type=['jpg', 'png'])

if 'engineered_prompt' not in st.session_state:
    st.session_state['engineered_prompt'] = ""

# 4. Step 1: Prompt Generation
st.subheader("Step 1: Generate Prompt")

if st.button("🚀 Step 1: Generate Prompt"):
    with st.spinner("Engineering prompt..."):
        # Construct the base text prompt
        prompt_text = (f"Create a professional {gen_type} for {platform}. "
                       f"Product: {product}. Shot: {shot_type}. Background: {background}. "
                       f"Lighting: {lighting}. Style: {style}. Rules: {', '.join(rules)}. {extra}")
        
        # Prepare content: include image only if it exists
        contents = [prompt_text]
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            contents.append(image)
        
        # Call the model
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=contents
            )
            st.session_state['engineered_prompt'] = response.text
            st.success("Prompt engineered!")
        except Exception as e:
            st.error(f"Error: {e}")

# 5. Step 2: Image Generation
if st.session_state['engineered_prompt']:
    st.subheader("Final Prompt Review")
    final_prompt = st.text_area("Edit if needed:", st.session_state['engineered_prompt'], height=150)
    
    if st.button("🎨 Step 2: Create Image"):
        with st.spinner("Generating image..."):
            try:
                # Use a model capable of image generation (e.g., imagen-3.0)
                # Note: Verify your specific API project access for image generation models
                result = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=final_prompt,
                    config=types.GenerateImagesConfig(number_of_images=1)
                )
                
                if result.generated_images:
                    for generated_image in result.generated_images:
                        image = Image.open(io.BytesIO(generated_image.image.image_bytes))
                        st.image(image, use_container_width=True)
                        st.download_button("📥 Download", generated_image.image.image_bytes, "roseey_result.png", "image/png")
                else:
                    st.error("No images returned.")

            except Exception as e:
                st.error(f"Error details: {e}")
