from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 5):
    try:
        results = []

        with DDGS(timeout=10) as ddgs:
            for item in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": item.get("title"),
                    "href": item.get("href"),
                    "body": item.get("body")
                })

        if not results:
            return {
                "text": "No web results found. Please check your internet connection and try again.",
                "sources": []
            }

        output = ""

        for idx, result in enumerate(results, start=1):
            output += f"{idx}. {result['title']}\n"
            output += f"{result['body']}\n"
            output += f"Link: {result['href']}\n\n"

        sources = [
            {
                "source": result["title"],
                "url": result["href"],
                "preview": result["body"]
            }
            for result in results
        ]

        return {
            "text": output.strip(),
            "sources": sources
        }

    except Exception as e:
        return {
            "text": f"Web search failed. Check your internet connection. Error: {str(e)}",
            "sources": []
        }
