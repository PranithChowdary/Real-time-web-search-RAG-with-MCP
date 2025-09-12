"""
Search tools for the MCP server.
Provides utility functions for handling search queries and results.
"""

def process_query(query: str) -> str:
    """
    Process the incoming query and prepare it for search.

    Args:
        query: The search query string.

    Returns:
        Processed query string.
    """
    return query.strip().lower()

def format_results(results: list) -> list:
    """
    Format search results for the client.

    Args:
        results: List of raw search results.

    Returns:
        List of formatted results.
    """
    return [{"title": r.get("title", "Untitled"), "url": r.get("url", "#")} for r in results]