import os
import streamlit as st
from groq import Groq

# Set page layout
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts for any platform with captions and hashtags.")

# Sidebar API Key configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

# User Input Controls
st.subheader("Content Parameters")

platform = st.selectbox(
    "Select Platform",
    ["LinkedIn", "Twitter / X", "Instagram", "Facebook", "Blog Post"]
)

content_type = st.selectbox(
    "Select Content Type",
    ["Educational / How-To", "Promotional / Sales", "Storytelling / Personal", "Industry Insights", "Announcement"]
)

tone = st.selectbox(
    "Select Tone",
    ["Professional", "Casual & Friendly", "Energetic & Inspiring", "Witty & Humorous", "Authoritative"]
)

target_audience = st.text_input("Target Audience", placeholder="e.g., Tech Founders, College Students, Fitness Enthusiasts")
topic = st.text_area("Topic / Main Idea", placeholder="e.g., Why learning Python in 2026 is still the best entry point for AI development")

# Content Generation Trigger
if st.button("Generate Post", type="primary"):
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not topic.strip():
        st.warning("Please provide a topic.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            prompt = f"""
You are an expert social media strategist and content creator.
Generate a complete post based on the following requirements:

- Platform: {platform}
- Content Type: {content_type}
- Tone: {tone}
- Target Audience: {target_audience if target_audience else 'General Audience'}
- Topic: {topic}

Provide the output formatted clearly as follows:
1. **Hook / Headline**
2. **Main Body Content** (Formatted appropriately for the chosen platform, e.g., thread for Twitter/X, clear paragraphs/bullet points for LinkedIn)
3. **Call to Action (CTA)**
4. **Hashtags** (5-10 highly relevant hashtags)
"""

            with st.spinner("Generating post..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                
            generated_content = response.choices[0].message.content
            
            st.success("Post Generated Successfully!")
            st.markdown("---")
            st.markdown(generated_content)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")