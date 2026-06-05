import streamlit as st
import google.generativeai as genai
from PIL import Image

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="AI Vision Prompt Generator",
    page_icon="📸",
    layout="centered"
)

# -----------------------------
# CONFIGURE GEMINI (Cached)
# -----------------------------
@st.cache_resource
def get_model():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    # Baking the quality rules into the model instructions permanently
    return genai.GenerativeModel(
        "gemini-3.5-flash",
        system_instruction=(
            "You are an elite expert prompt engineer and professional cinematographer. "
            "Your output must prioritize: 1. Anatomical perfection (5 fingers, correct joints, no morphing). "
            "2. Product integrity (geometric accuracy, no warping). 3. Cinematic realism (8k, sharp focus, "
            "proper depth of field). Never output artifacts or 'AI-look' distortions. "
            "Always use technical photography and cinematography terminology."
        )
    )

model = get_model()

st.title("📸 AI Vision Prompt Generator")
st.caption("Generate professional prompts from reference images.")

# -----------------------------
# SIDEBAR / FORM INPUT
# -----------------------------
with st.sidebar:
    st.header("Configure Prompt")
    
    with st.form("prompt_form"):
        platform = st.selectbox("📸 PLATFORM", ["ChatGPT Images", "Grok", "Gemini", "Midjourney", "Flux", "Veo", "Kling", "Hailuo", "Meta AI Video", "YouTube AI"])
        gen_type = st.selectbox("🎯 GENERATE", ["Photo Prompt", "Video Prompt", "Thumbnail Prompt", "Everything"])
        product = st.selectbox("📦 PRODUCT", ["Makeup", "Skincare", "Clothing", "Footwear", "Kitchenware", "Home Product", "Toy", "School Supply", "Electronics", "Other"])
        shot_type = st.selectbox("📷 SHOT TYPE", ["Product Close-up", "Handheld", "Mirror Selfie", "Mirror Video", "Lifestyle", "Full Body", "Half Body", "Feet Focus", "Hand Focus"])
        background = st.selectbox("🏠 BACKGROUND", ["Home", "Bedroom", "Living Room", "Kitchen", "Bathroom", "Vanity", "Laundry Area", "Cafe", "Street", "Garden", "Beach", "Pool", "Front Yard", "Studio", "Custom"])
        custom_bg = st.text_input("If 'Custom', describe it")
        lighting = st.selectbox("☀️ LIGHTING", ["Natural", "Bright Commercial", "Soft Studio", "Luxury", "Moody"])
        model_type = st.selectbox("🧍 MODEL", ["None", "Hand Only", "Feet Only", "Half Body", "Full Body", "Walking", "Sitting"])
        style = st.selectbox("✨ STYLE", ["UGC", "Product Showcase", "Modeling", "Lifestyle", "Problem-Solution", "Review"])
        aspect_ratio = st.selectbox("📐 ASPECT RATIO", ["9:16", "4:5", "1:1", "16:9"])
        rules = st.multiselect("📋 RULES", ["Design Lock", "Face Lock", "No Face", "No Script", "With Script"])
        extra = st.text_area("📝 EXTRA DETAILS")
        
        submitted = st.form_submit_button("🚀 GENERATE PROMPT")

# -----------------------------
# IMAGE INPUT
# -----------------------------
tab1, tab2 = st.tabs(["📸 Use Camera", "📁 Upload from Gallery"])
uploaded_file = None

with tab1:
    camera_file = st.camera_input("Take a photo")
    if camera_file: uploaded_file = camera_file

with tab2:
    gallery_file = st.file_uploader("Choose a photo", type=["jpg", "jpeg", "png"])
    if gallery_file: uploaded_file = gallery_file

# -----------------------------
# GENERATION LOGIC
# -----------------------------
if submitted and uploaded_file and model:
    image = Image.open(uploaded_file)
    st.image(image, caption="Reference Image", use_container_width=True)
    
    with st.spinner("Engineering high-fidelity prompt..."):
        final_bg = custom_bg if background == "Custom" else background
        rules_text = ", ".join(rules) if rules else "None"
        
        prompt_instructions = f"""
        Analyze the provided reference image. Generate a professional prompt based on these parameters:
        
        - Platform: {platform}
        - Type: {gen_type}
        - Product: {product}
        - Shot: {shot_type}
        - Background: {final_bg}
        - Lighting: {lighting}
        - Model: {model_type}
        - Style: {style}
        - Aspect Ratio: {aspect_ratio}
        - Rules: {rules_text}
        - Additional Details: {extra}

        INTERNAL VERIFICATION: Ensure the generated prompt contains specific technical keywords 
        to force the AI to avoid extra limbs, fused fingers, and distorted product geometry.
        Use professional lighting and camera lens terminology.
        """
        
        try:
            response = model.generate_content([prompt_instructions, image])
            st.success("Prompt generated successfully!")
            st.subheader("Generated Output")
            st.code(response.text, language="text")
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif submitted and not uploaded_file:
    st.warning("Please upload or take a photo first!")
elif submitted and not model:
    st.error("API Key not found. Please check your Streamlit secrets.")
