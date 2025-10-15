import pytest
from app_core import generate_questions

class FakeChain:
    """Minimal stand-in for LangChain's LLMChain for unit tests."""
    def __init__(self):
        self.last_inputs = None
        self.return_text = "Q1: Example?\nHint: <one-line hint>\nQ2: Another example?"
    def run(self, **kwargs):
        self.last_inputs = kwargs
        return self.return_text

def test_raises_on_empty_topic():
    fake = FakeChain()
    with pytest.raises(ValueError):
        generate_questions(
            topic="  ",
            count=7,
            difficulty=3,
            categories=["Fundamentals"],
            ensure_diversity=True,
            include_followups=True,
            chain=fake,
        )

def test_injects_followup_hint_when_enabled():
    fake = FakeChain()
    out = generate_questions(
        topic="Frontend Engineer",
        count=7,
        difficulty=3,
        categories=["Fundamentals", "Algorithms & DS"],
        ensure_diversity=True,
        include_followups=True,
        chain=fake,
    )
    # Verify the chain got the right flag and hint placeholder
    assert fake.last_inputs["followups_flag"] == "Yes"
    assert "Hint: <one-line hint>" in fake.last_inputs["hint_block_optional"]
    assert "Q1:" in out  # sanity check on fake return

def test_omits_followup_hint_when_disabled():
    fake = FakeChain()
    generate_questions(
        topic="Data Structures",
        count=7,
        difficulty=2,
        categories=["Algorithms & DS"],
        ensure_diversity=False,
        include_followups=False,
        chain=fake,
    )
    assert fake.last_inputs["followups_flag"] == "No"
    assert fake.last_inputs["hint_block_optional"] == ""

def test_category_join_and_diversity_flag():
    fake = FakeChain()
    generate_questions(
        topic="SRE",
        count=6,
        difficulty=4,
        categories=["System Design", "Behavioral"],
        ensure_diversity=True,
        include_followups=True,
        chain=fake,
    )
    assert fake.last_inputs["categories"] == "System Design, Behavioral"
    assert "cover distinct subtopics" in fake.last_inputs["diversity_flag"]

def test_category_any_when_none():
    fake = FakeChain()
    generate_questions(
        topic="Python",
        count=5,
        difficulty=1,
        categories=[],
        ensure_diversity=False,
        include_followups=False,
        chain=fake,
    )
    assert fake.last_inputs["categories"] == "Any"

@pytest.mark.parametrize("requested,expected", [(3,5),(5,5),(10,10),(12,10)])
def test_count_is_clamped_5_to_10(requested, expected):
    fake = FakeChain()
    generate_questions(
        topic="Backend Engineer",
        count=requested,
        difficulty=3,
        categories=None,
        ensure_diversity=False,
        include_followups=False,
        chain=fake,
    )
    assert fake.last_inputs["count"] == expected

@pytest.mark.parametrize("requested,expected", [(0,1),(1,1),(5,5),(7,5)])
def test_difficulty_is_clamped_1_to_5(requested, expected):
    fake = FakeChain()
    generate_questions(
        topic="Security Engineer",
        count=7,
        difficulty=requested,
        categories=None,
        ensure_diversity=False,
        include_followups=False,
        chain=fake,
    )
    assert fake.last_inputs["difficulty"] == expected
