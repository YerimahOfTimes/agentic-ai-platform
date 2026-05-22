from app.llm import llm
from app.memory import format_memory


def clean_output(text):
    unwanted_phrases = [
        "Your final answer",
        "final answer is as follows",
        "you are a professional",
        "assistant who has mastered",
        "Congratulations on passing",
        "Please be sure to follow",
        "You are an AI that only outputs the final answer",
        "meets all of the formatting requirements"
    ]

    for phrase in unwanted_phrases:
        text = text.replace(phrase, "")

    return text.strip()


def writer_agent(state):
    print("✍ Writer running...")

    if "trace" not in state:
        state["trace"] = []

    if state.get("tool_output"):
        state["trace"].append("Writer returned tool output")
        print("✅ Writer finished")
        return {
            "final_answer": state["tool_output"],
            "sources": state.get("sources", []),
            "trace": state.get("trace", [])
        }

    context = state.get("context", "")
    question = state["question"]
    session_id = state.get("session_id", "default")
    memory = format_memory(session_id)

    prompt = prompt = f"""
Answer briefly using the context.

Context:
{context}

Question:
{question}

Answer in 3 sentences max:
"""

    final = llm.invoke(prompt)
    final_text = final.content if hasattr(final, "content") else str(final)
    cleaned = clean_output(final_text)

    state["trace"].append("Writer generated final answer")

    print("✅ Writer finished")

    return {
        "final_answer": cleaned,
        "sources": state.get("sources", []),
        "trace": state.get("trace", [])
    }
