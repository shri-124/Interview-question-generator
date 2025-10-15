from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

SYSTEM_PROMPT = """You are an expert interviewer and question crafter.
You generate concise, high-quality interview questions tailored to the given role/topic and difficulty.

Guidelines:
- Questions must be crisp and atomic (no multi-part numbered sub-questions).
- Calibrate difficulty on a 1–5 scale (1=easiest, 5=hardest).
- Prefer practical, real-world scenarios for applied roles.
- Avoid repeating the same concept; aim for coverage across skills.
- Do not include answers unless explicitly asked.
"""

USER_PROMPT_TEMPLATE = """
Create {count} interview questions for the role/topic: "{topic}".

Difficulty target: {difficulty}/5.
Categories to cover: {categories}.
Diversity requirement: {diversity_flag}.
Include a short follow-up hint after each question: {followups_flag}.

Format strictly as:
Q1: <question>
{hint_block_optional}
Q2: <question>
{hint_block_optional}
...
"""

_prompt = PromptTemplate(
    template=USER_PROMPT_TEMPLATE.strip(),
    input_variables=[
        "count", "topic", "difficulty", "categories",
        "diversity_flag", "followups_flag", "hint_block_optional"
    ],
)

def _make_chain(temperature: float, model_name: str) -> LLMChain:
    llm = ChatOpenAI(model=model_name, temperature=temperature)
    return LLMChain(llm=llm, prompt=_prompt, verbose=False)

def _normalize_inputs(
    topic: str,
    count: int,
    difficulty: int,
    categories: Optional[List[str]],
    ensure_diversity: bool,
    include_followups: bool,
):
    if not topic or not topic.strip():
        raise ValueError("topic is required")
    # Constrain UI expectations (5–10) just in case callers bypass the UI
    count = max(5, min(10, int(count)))
    difficulty = max(1, min(5, int(difficulty)))

    cat_str = ", ".join(categories) if categories else "Any"
    diversity_flag = (
        "Yes, cover distinct subtopics and avoid overlaps."
        if ensure_diversity else
        "Not required."
    )
    followups_flag = "Yes" if include_followups else "No"
    hint_block_optional = "Hint: <one-line hint>" if include_followups else ""

    return {
        "count": count,
        "topic": topic.strip(),
        "difficulty": difficulty,
        "categories": cat_str,
        "diversity_flag": diversity_flag,
        "followups_flag": followups_flag,
        "hint_block_optional": hint_block_optional,
    }

def generate_questions(
    *,
    topic: str,
    count: int,
    difficulty: int,
    categories: Optional[List[str]],
    ensure_diversity: bool,
    include_followups: bool,
    temperature: float = 0.5,
    model_name: str = "gpt-4o-mini",
    chain: Optional[LLMChain] = None,  # injected in tests
) -> str:
    """Return generated questions text. Raises ValueError on invalid inputs."""
    inputs = _normalize_inputs(
        topic, count, difficulty, categories, ensure_diversity, include_followups
    )
    use_chain = chain or _make_chain(temperature, model_name)
    return use_chain.run(**inputs)
