from dotenv import load_dotenv
from app.agent import build_agent

load_dotenv()

agent = build_agent()

def test_simple_calculation():
    response = agent.invoke("Quanto é 2 + 2?")
    assert response == "4"

def test_operator_precedence():
    response = agent.invoke("Quanto é 1 + 2 * 3?")
    assert response == "7"

def test_general_knowledge_pt():
    response = agent.invoke("Quem foi Albert Einstein?")
    assert "Einstein" in response

def test_general_knowledge_en():
    response = agent.invoke("Who was Albert Einstein?")
    assert "Einstein" in response

def test_mixed_intent():
    response = agent.invoke("Quanto é 2 + 2 e quem foi Albert Einstein?")
    assert response.lower().startswith("reject")

def test_escaped_operator():
    response = agent.invoke("Quanto é 10 * 2?")
    assert response == "20"

def test_invalid_expression():
    response = agent.invoke("Quanto é 2 ++ 2?")
    assert response.lower().startswith("reject")

def test_non_math_expression():
    response = agent.invoke("Quanto é a capital da França?")
    assert response.lower().startswith("reject")

def test_non_numeric_expression():
    response = agent.invoke("Quanto é dois mais dois?")
    assert response == "4" 




