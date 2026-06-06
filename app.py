import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# -----------------------------
# CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Roseey Personalized Generator",
    page_icon="📸",
    layout="centered"
)

# Initialize Client
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)

# Persistent storage for the generated prompt
if 'engineered_prompt' not in st.session_state:
    st.session_state['engineered_prompt'] = ""

st.title("📸 Roseey Personalized Generator")
st.caption("Step 1: Generate Prompt | Step 2: Create Image")

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.header("1. Configure Context")
    
    with st.form("context_form"):
        # Existing Options
        platform = st.selectbox("📸 PLATFORM", ["ChatGPT Images", "Grok", "Gemini", "Midjourney", "Flux", "Veo", "Kling", "Hailuo", "Meta AI Video", "YouTube AI"])
        gen_type = st.selectbox("🎯 GENERATE", ["Photo Prompt", "Video Prompt", "Thumbnail Prompt", "Everything"])
        product = st.selectbox("📦 PRODUCT", ["Makeup", "Skincare", "Clothing", "Footwear", "Kitchenware", "Home Product", "Toy", "School Supply", "Electronics", "Other"])
        shot_type = st.selectbox("📷 SHOT TYPE", ["Product Close-up", "Handheld", "Mirror Selfie", "Mirror Video", "Lifestyle", "Full Body", "Half Body", "Feet Focus", "Hand Focus"])
        background = st.selectbox("🏠 BACKGROUND", ["Home", "Bedroom", "Living Room", "Kitchen", "Bathroom", "Vanity", "Laundry Area", "Cafe", "Street", "Garden", "Beach", "Pool", "Front Yard", "Studio", "Custom"])
        custom_bg = st.text_input("If 'Custom', describe background")
        lighting = st.selectbox("☀️ LIGHTING", ["Natural", "Bright Commercial", "Soft Studio", "Luxury", "Moody"])
        model_type = st.selectbox("🧍 MODEL", ["None", "Hand Only", "Feet Only", "Half Body", "Full Body", "Walking", "Sitting"])
        style = st.selectbox("✨ STYLE", ["UGC", "Product Showcase", "Modeling", "Lifestyle", "Problem-Solution", "Review"])
        aspect_ratio = st.selectbox("📐 ASPECT RATIO", ["9:16", "4:5", "1:1", "16:9"])
        extra = st.text_area("📝 EXTRA DETAILS")
        
        # New Rule Toggles
        anatomical_correctness = st.checkbox("Strict Anatomy", value=True)
        structural_integrity = st.checkbox("Structural Integrity", value=True)

        st.form_submit_button("Reset Configuration")

# -----------------------------
# MAIN CONTENT
# -----------------------------
tab1, tab2 = st.tabs(["📁 Reference Input", "🎨 Image Creation"])

with tab1:
    uploaded_files = st.file_uploader(
        "Upload Reference Images (Context Only)", 
        type=["jpg", "png"], 
        accept_multiple_files=True
    )
    
    # 1. GENERATE PROMPT (Analyzing uploaded image context)
    if st.button("🚀 Step 1: Generate Prompt"):
        if not uploaded_files:
            st.warning("Please upload reference images first.")
        elif not api_key:
            st.error("API Key not found.")
        else:
            with st.spinner("Analyzing image and engineering prompt..."):
                final_bg = custom_bg if background == "Custom" else background
                
                prompt_instructions = (
                    f"Create a professional {gen_type} for {platform}. Category: {product}, Shot: {shot_type}, BG: {final_bg}, Lighting: {lighting}, Model: {model_type}, Style: {style}, Aspect: {aspect_ratio}. Extra: {extra}. "
                )
                
                if anatomical_correctness:
                    prompt_instructions += "TECHNICAL RULES: Ensure anatomical perfection. "
                if structural_integrity:
                    prompt_instructions += "Ensure structural integrity. "

                contents = [prompt_instructions]
                for file in uploaded_files:
                    contents.append(Image.open(file))
                
                try:
                    # Generate the engineered prompt text using Gemini Pro (for analysis)
                    response = client.models.generate_content(model="gemini-1.5-pro", contents=contents)
                    st.session_state['engineered_prompt'] = response.text
                    st.success("Step 1 Complete: Prompt engineered below.")
                except Exception as e:
                    st.error(f"Error engineering prompt: {e}")

with tab2:
    # 2. CREATE IMAGE (Using the engineered prompt)
    if st.session_state['engineered_prompt']:
        st.subheader("Engineered Prompt (Step 1 Output)")
        
        with st.form("image_form"):
            # Display the prompt in an editable text area
            final_prompt_text = st.text_area("Review or edit the prompt:", st.session_state['engineered_prompt'], height=200)
            
            # Button 2: Triggers the Image model
            create_image_submitted = st.form_submit_button("🎨 Step 2: Create Image")

        if create_image_submitted:
            if not final_prompt_text:
                st.warning("Please generate or enter a prompt first.")
            else:
                with st.spinner("Creating image with Gemini Image API..."):
                    try:
                        # Use the appropriate Image model (e.g., imagen-3.0-generate-002)
                        img_response = client.models.generate_images(
                            model='imagen-3.0-generate-002',
                            prompt=final_prompt_text,
                            config=types.GenerateImagesConfig(number_of_images=1)
                        )
                        
                        for generated_image in img_response.generated_images:
                            img_bytes = generated_image.image.image_bytes
                            image = Image.open(io.BytesIO(img_bytes))
                            
                            st.image(image, caption="Generated Result", use_container_width=True)
                            
                            # Download Button for the resulting image bytes
                            st.download_button(
                                label="📥 Download Image",
                                data=img_bytes,
                                file_name="roseey_generated.png",
                                mime="image/png"
                            )
                    except Exception as e:
                        st.error(f"Image creation failed: {e}")
    else:
        st.info("Complete Step 1 (Generate Prompt) in the Reference Input tab to proceed to image creation.")
