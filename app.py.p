import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Email Generator", page_icon="✉️", layout="centered")

st.title("✉️ AI Email Generator")
st.caption("Generate professional emails with Groq AI.")

# Works with Streamlit Cloud secrets or a local environment variable.
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

if not api_key:
    st.error("GROQ_API_KEY is not configured. Add it to Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

with st.form("email_form"):
    email_type = st.selectbox(
        "Email type",
        [
            "Professional Email",
            "Follow-up Email",
            "Thank-you Email",
            "Job Application Email",
            "Meeting Request",
            "Apology Email",
            "Custom Email",
        ],
    )

    recipient = st.text_input("Recipient / audience", placeholder="e.g. Client, Manager, Professor")
    purpose = st.text_area(
        "Purpose / main idea",
        placeholder="Describe what you want to say...",
        height=120,
    )

    tone = st.selectbox(
        "Tone",
        ["Professional", "Friendly", "Formal", "Concise", "Persuasive"],
    )

    language = st.selectbox("Language", ["English", "Urdu", "Roman Urdu"])

    length = st.selectbox("Length", ["Short", "Medium", "Detailed"])

    submitted = st.form_submit_button("Generate Email", use_container_width=True)

if submitted:
    if not purpose.strip():
        st.warning("Please enter the purpose or main idea.")
        st.stop()

    prompt = f"""
You are an expert email writer.

Write a complete {email_type.lower()}.

Recipient/audience: {recipient or "Not specified"}
Purpose/main idea: {purpose}
Tone: {tone}
Language: {language}
Length: {length}

Requirements:
- Include a clear subject line.
- Write only the email, not an explanation.
- Keep the wording natural and professional.
- Do not invent personal details, dates, prices, names, or commitments.
"""

    try:
        with st.spinner("Generating your email..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b"
                    {
                        "role": "system",
                        "content": "You write high-quality, clear emails for users.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=800,
            )

        email = response.choices[0].message.content.strip()

        st.subheader("Generated Email")
        st.text_area("Copy your email", value=email, height=350)

    except Exception as e:
        st.error(f"Generation failed: {e}")
