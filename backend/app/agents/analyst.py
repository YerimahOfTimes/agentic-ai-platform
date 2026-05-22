from app.llm import llm


def analyst_agent(state):
    print("📊 Analyst running...")

    prompt = f"""
    Analyze the question carefully and explain it clearly.

    Question:
    {state['question']}

    Context:
    {state.get('context', '')}
    """

    analysis = llm.invoke(prompt)

    print("✅ Analyst finished")

    return {"analysis": analysis}
