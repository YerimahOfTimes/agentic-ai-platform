from typing import TypedDict, Optional, Any, List


class AgentState(TypedDict, total=False):
    # 🔹 User input
    question: str

    # 🔹 Supervisor routing decision
    next_agent: Optional[str]

    # 🔹 Shared working memory
    context: Optional[str]
    analysis: Optional[str]
    tool_output: Optional[str]
    final_answer: Optional[str]

    # 🔹 Optional agent outputs (for debugging / observability)
    retriever_output: Optional[str]
    writer_output: Optional[str]

    sources: List[Any]

    # 🔹 Conversation / memory layer (future-ready)
    messages: List[Any]

    trace: List[str]

    # 🔹 Metadata (useful for tracing later)
    step: Optional[str]

    session_id: Optional[str]
