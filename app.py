import streamlit as st
import google.generativeai as genai
from PIL import Image

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Roseey Personalized Generator",
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
    # Model initialized with core "Hidden Rules" for accuracy and physics
    return genai.GenerativeModel(
        "gemini-3.5-flash",
        system_instruction=(
            "You are an expert AI cinematographic director and prompt engineer. "
            "STRICT RULES: "
            "1. ANATOMY: Absolute correctness (5 fingers, natural joints, no warping). "
            "2. PHYSICS & MOTION: Movements must obey laws of physics, maintain gravity/weight distribution. "
            "3. PRODUCT: Maintain structural integrity, no warping. "
            "4. TERMINOLOGY: Use professional 8k cinematography and animation vocabulary."
        )
    )

model = get_model()

st.title("📸 Roseey Personalized Generator")
st.caption("Generate professional, personalized prompts from reference images.")

# -----------------------------
# SIDEBAR / FORM INPUT
# -----------------------------
with st.sidebar:
    st.header("Configure Prompt")
    
    with st.form("prompt_form"):
        platform = st.selectbox("📸 PLATFORM", ["ChatGPT Images", "Grok", "Gemini", "Midjourney", "Flux", "Veo", "Kling", "Hailuo", "Meta AI Video", "YouTube AI"])
        gen_type = st.selectbox("🎯 GENERATE", ["Photo Prompt", "Video Prompt", "Thumbnail Prompt", "Everything"])
        
        voiceover = st.selectbox("🎙️ VOICEOVER", ["No Voiceover", "Native Filipina Speaker", "English Speaker", "Custom Language"])
        custom_lang = st.text_input("If 'Custom Language', specify here:")

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
# IMAGE INPUT (Multiple)
# -----------------------------
uploaded_files = st.file_uploader(
    "📁 Upload Reference Images", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

# -----------------------------
# GENERATION LOGIC
# -----------------------------
if submitted and uploaded_files and model:
    # Display uploaded images
    cols = st.columns(min(len(uploaded_files), 3))
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        cols[i % 3].image(img, use_container_width=True)
    
    with st.spinner("Engineering high-fidelity prompt..."):
        final_bg = custom_bg if background == "Custom" else background
        rules_text = ", ".join(rules) if rules else "None"
        selected_voice = f"{voiceover} ({custom_lang})" if voiceover == "Custom Language" else voiceover
        
        # Build prompt instructions
        prompt_instructions = f"""
        Analyze these reference images. Generate a professional prompt based on these parameters:
        
        - Platform: {platform}
        - Voiceover Preference: {selected_voice}
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

        BODY MECHANICS: Ensure all movements (walking, sitting, hand gestures) are fluid, biomechanically accurate, and grounded in physics.
        INTERNAL VERIFICATION: Avoid anatomical errors (extra fingers, limbs) and warped geometry.
        """
        
        # Prepare content list (Prompt + Images)
        contents = [prompt_instructions]
        for file in uploaded_files:
            contents.append(Image.open(file))
        
        try:
            response = model.generate_content(contents)
            st.success("Prompt generated successfully!")
            st.subheader("Generated Output")
            st.code(response.text, language="text")
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif submitted and not uploaded_files:
    st.warning("Please upload at least one image first!")
elif submitted and not model:
    st.error("API Key not found. Please check your Streamlit secrets.")
