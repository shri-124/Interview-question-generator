import os
import streamlit as st
from dotenv import load_dotenv
from app_core import generate_questions

if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

DEMO_MODE = not bool(os.getenv("OPENAI_API_KEY"))

load_dotenv()
st.set_page_config(page_title="Interview Question Generator", page_icon="🧠", layout="centered")

st.title("🧠 Interview Question Generator")
st.caption("Powered by LangChain + OpenAI. App is in DEMO MODE to save tokens and all responses are pre written from ChatGPT.")

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
            if DEMO_MODE:
                # simple offline fake output so the UI still works
                demo = ["Explain the difference between server-side rendering (SSR) and client-side rendering (CSR) in Next.js. When would you choose one over the other?",
                        "How does React's virtual DOM improve performance?", "What are React hooks? Can you describe how useEffect and useMemo differ?",
                        "Walk me through how you would design a REST API endpoint for a “user signup” feature. How would you handle input validation, password security, and error responses?",
                        "What are middleware functions in Express.js, and how are they typically used?",
                        "How would you debug a production API that occasionally returns 500 errors with no clear logs?",
                        "Compare SQL and NoSQL databases. When would you pick one over the other?",
                        "How would you integrate Redis or another caching system to improve performance?",
                        "Describe a time you built and deployed a full-stack application end-to-end. What challenges did you face and how did you overcome them?",
                        "How do you handle version control, code reviews, and CI/CD in your development workflow?",
                        "How do you ensure your code is maintainable and testable in a large project?"
                        ]
                for i in range(1, count + 1):
                    q = f"Q{i}: ({difficulty}/5) Draft a question related to '{topic}' " \
                        f"covering {', '.join(categories) if categories else 'general fundamentals'}."
                    if include_followups:
                        q += "\nHint: Think about core principles and trade-offs."
                    demo.append(q)
                result = "\n\n".join(demo)
            else:
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
