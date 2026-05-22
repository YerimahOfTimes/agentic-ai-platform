from langgraph.graph import StateGraph, END

from app.graph.state import AgentState

from app.agents.supervisor import supervisor_agent
from app.agents.retriever import retriever_agent
from app.agents.analyst import analyst_agent
from app.agents.writer import writer_agent
from app.agents.tool_agent import tool_agent


def router(state):
    return state["next_agent"]


graph = StateGraph(AgentState)

graph.add_node("supervisor", supervisor_agent)
graph.add_node("retriever", retriever_agent)
graph.add_node("analyst", analyst_agent)
graph.add_node("writer", writer_agent)
graph.add_node("tool", tool_agent)

graph.set_entry_point("supervisor")

graph.add_conditional_edges(
    "supervisor",
    router,
    {
        "retriever": "retriever",
        "analyst": "analyst",
        "writer": "writer",
        "tool": "tool",
    }
)

graph.add_edge("retriever", "writer")
graph.add_edge("analyst", "writer")
graph.add_edge("tool", "writer")

graph.add_edge("writer", END)

workflow = graph.compile()
