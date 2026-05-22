import re
from app.llm import llm


def supervisor_agent(state):
    if "trace" not in state:
        state["trace"] = []

    state["trace"].append("Supervisor started")

    question = state["question"]
    q = question.lower()

    if "python" in q:
        state["next_agent"] = "tool"
        state["trace"].append("Routed to tool: python")
        return state

    if re.search(r"\d+\s*[\+\-\*\/]\s*\d+", q):
        state["next_agent"] = "tool"
        state["trace"].append("Routed to tool: calculator")
        return state

    if any(word in q for word in ["search", "latest", "current", "today", "news", "web"]):
        state["next_agent"] = "tool"
        state["trace"].append("Routed to tool: web search")
        return state

    if any(word in q for word in ["sql", "database", "employees", "employee", "salary", "table"]):
        state["next_agent"] = "tool"
        state["trace"].append("Routed to tool: sql")
        return state

    if any(word in q.split() for word in ["he", "she", "they", "it", "this", "that", "his", "her", "their"]):
        state["next_agent"] = "retriever"
        state["trace"].append("Routed to retriever: follow-up question")
        return state

    if any(word in q for word in ["what is", "define", "explain", "meaning of", "skill", "skills", "experience", "project", "cv", "resume", "file", "document"]):
        state["next_agent"] = "retriever"
        state["trace"].append("Routed to retriever")
        return state

    prompt = f"""
Choose one agent.

Agents:
retriever
analyst
writer
tool

Return only one word.

Question:
{question}
"""

    response = llm.invoke(prompt).content.strip().lower()

    valid_agents = ["retriever", "analyst", "writer", "tool"]

    if response not in valid_agents:
        response = "writer"

    state["next_agent"] = response
    state["trace"].append(f"Routed to {response}")

    return state
