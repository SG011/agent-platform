import httpx

WEB_SEARCH_TOOL = {
    "name": "web_search",
    "description": "Search the web for current information on a topic",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string", "description": "Search query"}},
        "required": ["query"]
    }
}


def web_search_handler(query: str) -> str:
    try:
        resp = httpx.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": "1"},
            timeout=10
        )
        data = resp.json()
        abstract = data.get("AbstractText", "")
        return abstract if abstract else f"No instant answer found for: {query}"
    except Exception as e:
        return f"Search failed: {e}"
