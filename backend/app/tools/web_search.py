from duckduckgo_search import DDGS


def clean_search_query(question: str):
    q = question.lower().strip()

    remove_words = [
        "search for",
        "search",
        "web search",
        "look up",
        "find",
    ]

    for word in remove_words:
        q = q.replace(word, "")

    return q.strip()


def format_results(results):
    if not results:
        return {
            "text": "No web results found. Please check your internet connection and try again.",
            "sources": []
        }

    output = ""

    sources = []

    for idx, result in enumerate(results, start=1):
        title = result.get("title", "No title")
        url = result.get("url") or result.get("href", "")
        body = result.get("body", "")

        output += f"{idx}. {title}\n"
        output += f"{body}\n"
        output += f"Link: {url}\n\n"

        sources.append({
            "source": title,
            "url": url,
            "preview": body
        })

    return {
        "text": output.strip(),
        "sources": sources
    }


def web_search(question: str, max_results: int = 5):
    query = clean_search_query(question)

    try:
        with DDGS(timeout=20) as ddgs:

            # NEWS SEARCH FIRST
            if any(word in query for word in ["latest", "today", "news", "current"]):
                news_results = list(
                    ddgs.news(
                        query,
                        max_results=max_results
                    )
                )

                if news_results:
                    return format_results(news_results)

            # NORMAL SEARCH FALLBACK
            text_results = list(
                ddgs.text(
                    query,
                    max_results=max_results
                )
            )

            return format_results(text_results)

    except Exception as e:
        return {
            "text": f"Web search failed. Check your internet connection. Error: {str(e)}",
            "sources": []
        }
