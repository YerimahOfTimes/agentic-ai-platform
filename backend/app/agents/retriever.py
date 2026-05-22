from app.rag.vectorstore import get_vector_db


def retriever_agent(state):
    print("📚 Retriever running...")

    if "trace" not in state:
        state["trace"] = []

    vector_db = get_vector_db()

    if vector_db is None:
        state["context"] = "No document has been uploaded yet."
        state["sources"] = []
        state["trace"].append("Retriever found no FAISS index")
        return state

    results = vector_db.similarity_search_with_score(
        state["question"],
        k=5
    )

    filtered_docs = []

    for doc, score in results:
        print(f"📊 SCORE: {score}")

        if score < 3.0:
            filtered_docs.append(doc)

    if not filtered_docs:
        state["context"] = "No relevant information found."
        state["sources"] = []
        state["trace"].append("Retriever found no relevant documents")
        return state

    context = "\n\n".join([doc.page_content for doc in filtered_docs])

    sources = []

    for doc in filtered_docs:
        sources.append({
            "source": doc.metadata.get("source", "unknown"),
            "preview": doc.page_content[:150]
        })

    state["context"] = context
    state["sources"] = sources
    state["trace"].append("Retriever searched FAISS index")

    print("✅ Retriever finished")

    return state
