import re

from app.tools.calculator import calculator_tool
from app.tools.python_tool import run_python_code
from app.tools.web_search import web_search
from app.tools.sql_tool import run_sql_query, run_natural_sql


def tool_agent(state):
    print("🛠 Tool agent running...")

    if "trace" not in state:
        state["trace"] = []

    question = state["question"]
    q = question.lower()

    if "python" in q:
        code = q.replace("python", "").strip()

        result = run_python_code(code)

        state["tool_output"] = result
        state["final_answer"] = result
        state["sources"] = []
        state["trace"].append("Used Python execution tool")

        print("✅ Python tool used")
        return state

    if any(word in q for word in ["search", "latest", "current", "today", "news", "web"]):
        result = web_search(question)

        state["tool_output"] = result["text"]
        state["final_answer"] = result["text"]
        state["sources"] = result["sources"]
        state["trace"].append("Used web search tool")

        print("✅ Web search tool used")
        return state

    if any(word in q for word in ["sql", "database", "employees", "employee", "salary", "table"]):
        if q.strip().startswith("sql"):
            query = question.replace("sql", "", 1).strip()
            result = run_sql_query(query)
        else:
            result = run_natural_sql(question)

        state["tool_output"] = result
        state["final_answer"] = result
        state["sources"] = []
        state["trace"].append("Used SQL database tool")

        print("✅ SQL tool used")
        return state

    if re.search(r"\d+\s*[\+\-\*\/]\s*\d+", question):
        result = calculator_tool(question)

        state["tool_output"] = result
        state["final_answer"] = result
        state["sources"] = []
        state["trace"].append("Used calculator tool")

        print("✅ Calculator tool used")
        return state

    state["tool_output"] = "No suitable tool found."
    state["final_answer"] = state["tool_output"]
    state["sources"] = []
    state["trace"].append("No suitable tool found")

    print("✅ Tool agent finished")
    return state
