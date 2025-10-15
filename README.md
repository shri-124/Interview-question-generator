# 🧠 Interview Question Generator

A simple **LangChain + Streamlit** app that automatically generates interview questions tailored to a **job title** or **technical topic** — with adjustable difficulty and question count. AT THE MOMENT I HAVE REMOVED THE API KEY TO NOT WASTE TOKENS

This project is ideal as a **1-day LangChain demo** that showcases:
- LLMChain + PromptTemplate
- Parameterized prompts
- A clean Streamlit interface
- Basic testing via pytest

---

## 🚀 Features

✅ Generate **5–10** interview questions  
✅ Control **difficulty (1–5)** and **creativity (temperature)**  
✅ Optional **follow-up hints** for each question  
✅ Ensure **topic diversity** across categories  
✅ Choose from pre-defined categories like Fundamentals, Algorithms, System Design, etc.  
✅ Export results as `.txt`  
✅ Fully tested using `pytest` with a `FakeChain` for offline testing  

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| UI | [Streamlit](https://streamlit.io/) |
| LLM Framework | [LangChain](https://python.langchain.com) |
| Model | OpenAI (GPT-4o, GPT-3.5-Turbo, etc.) |
| Env Config | python-dotenv |
| Testing | pytest |

---

## 🏗️ Folder Structure

interview-gen/
├─ app.py # Streamlit UI
├─ app_core.py # Core logic for generation
├─ tests/
│ └─ test_app_core.py # Unit tests (pytest)
├─ requirements.txt
├─ requirements-dev.txt
└─ .env