import os
import streamlit as st
from dotenv import load_dotenv
from app_core import generate_questions

load_dotenv()
st.set_page_config(page_title="Interview Question Generator", page_icon="🧠", layout="centered")

st.title("🧠 Interview Question Generator")
st.caption("Powered by LangChain + OpenAI")

with st.sidebar:
    st.header("Controls")
    topic = st.text_input("Job title or topic", placeholder="e.g., Frontend Engineer, Data Structures")
    count = st.slider("Number of questions", 5, 10, 7, 1)
    difficulty = st.slider("Difficulty (1 = easy, 5 = hard)", 1, 5, 3)
    categories = st.multiselect(
        "Categories (optional)",
        ["Fundamentals", "Algorithms & DS", "System Design", "Language/Framework", "Behavioral"],
        default=["Fundamentals", "Algorithms & DS"],
    )
    include_followups = st.checkbox("Include 1 follow-up hint per question", value=True)
    ensure_diversity = st.checkbox("Ensure topic diversity", value=True)
    temperature = st.slider("Creativity (temperature)", 0.0, 1.2, 0.5, 0.1)
    model_name = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-4.1", "gpt-3.5-turbo"], index=0)

if st.button("Generate Questions", type="primary", use_container_width=True):
    try:
        with st.spinner("Crafting questions..."):
            result = generate_questions(
                topic=topic,
                count=count,
                difficulty=difficulty,
                categories=categories,
                ensure_diversity=ensure_diversity,
                include_followups=include_followups,
                temperature=temperature,
                model_name=model_name,
            )
        st.subheader("Generated Questions")
        st.write(result)
        st.download_button(
            "Download as text",
            data=result,
            file_name=f"{(topic or 'questions').replace(' ', '_').lower()}_questions.txt",
            mime="text/plain",
            use_container_width=True,
        )
    except ValueError as e:
        st.error(str(e))

with st.expander("Tips"):
    st.markdown(
        """
- Use **Difficulty 1–2** for screening, **3** for mid-levels, **4–5** for senior/lead.
- Toggle **diversity** on to avoid duplicates.
- Add **Behavioral** to mix in STAR-style prompts.
- Raise **temperature** for more creative scenarios; lower for tight phrasing.
        """.strip()
    )
