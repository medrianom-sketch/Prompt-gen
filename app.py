import streamlit as st

st.set_page_config(page_title="AI Prompt Generator", layout="wide")
st.title("🚀 AI Prompt Engineering Tool")

# Sidebar - Categories
st.sidebar.header("Configure Prompt")
platform = st.sidebar.selectbox("📸 PLATFORM", ["ChatGPT", "Grok", "Gemini", "Midjourney", "Flux", "Veo", "Kling", "Hailuo", "Meta AI Video", "YouTube"])
gen_type = st.sidebar.selectbox("🎯 GENERATE", ["Photo Prompt", "Video Prompt", "Thumbnail Prompt"])
product = st.sidebar.text_input("📦 PRODUCT")
shot_type = st.sidebar.selectbox("📷 SHOT TYPE", ["Product Close-up", "Handheld", "Mirror Selfie", "Mirror Video", "Lifestyle", "Full Body", "Half Body", "Feet Focus", "Hand Focus"])
background = st.sidebar.selectbox("🏠 BACKGROUND", ["Home", "Kitchen", "Studio", "Cafe", "Street", "Garden", "Beach", "Pool"])
lighting = st.sidebar.selectbox("☀️ LIGHTING", ["Natural", "Bright Commercial", "Soft Studio", "Luxury", "Moody"])
model = st.sidebar.selectbox("🧍 MODEL", ["None", "Hand Only", "Feet Only", "Half Body", "Full Body", "Walking", "Sitting"])
style = st.sidebar.selectbox("✨ STYLE", ["UGC", "Product Showcase", "Modeling", "Lifestyle", "Problem-Solution", "Review"])
rules = st.sidebar.multiselect("📋 RULES", ["Design Lock", "Face Lock", "No Face", "No Script", "With Script"])
extra = st.sidebar.text_area("📝 EXTRA DETAILS")

# Main Page - Generation
if st.button("GENERATE PROMPT"):
    st.subheader("Your AI Prompt:")
    prompt = f"Platform: {platform} | Task: {gen_type} | Product: {product} | Shot: {shot_type} | Background: {background} | Lighting: {lighting} | Model: {model} | Style: {style} | Rules: {', '.join(rules)} | Details: {extra}"
    st.code(prompt, language='text')
    st.success("Prompt generated!")
