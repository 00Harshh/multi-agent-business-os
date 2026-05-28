"""
Agent tools for Pinecone vector database operations.
"""
import asyncio
from crewai.tools import tool
from business_os.tools.scraper_bot import get_pinecone_index, get_embedding, crawl_and_index_website
from business_os.config.settings import settings


@tool("Query Pinecone Knowledge Base")
def query_pinecone_knowledge(query: str) -> str:
    """Search the scraped vector database for deep business insights, tech stack details,
    pricing models, products, or pain points of target companies.
    """
    if not settings.pinecone_api_key:
        return "ERROR: Pinecone API Key is not configured. Cannot perform query."

    try:
        # Get query embedding
        query_vector = get_embedding(query)

        # Get index
        index = get_pinecone_index()

        # Query Pinecone with reduced top_k to keep context small and highly relevant for cheap models
        results = index.query(
            vector=query_vector,
            top_k=3,
            include_metadata=True
        )

        matches = results.get("matches", [])
        if not matches:
            return f"No relevant information found in vector memory for query: '{query}'"

        formatted_matches = []
        for match in matches:
            metadata = match.get("metadata", {})
            score = match.get("score", 0.0)
            url = metadata.get("url", "Unknown Source")
            title = metadata.get("title", "Untitled")
            content = metadata.get("content", "")
            
            formatted_matches.append(
                f"--- Result from: {title} ({url}) [Relevance: {score:.2f}] ---\n"
                f"{content}\n"
            )

        return "\n".join(formatted_matches)

    except Exception as e:
        return f"Error querying Pinecone database: {e}"


@tool("Scrape and Index Website to Pinecone")
def scrape_and_learn_website(url: str) -> str:
    """Crawls a website using Crawl4AI, chunks the text, embeds it, and saves it
    to the Pinecone vector memory so that other tools can query it later.
    Use this to dynamically research any company or directory you discover.
    """
    if not settings.pinecone_api_key:
        return "ERROR: Pinecone API Key is not configured. Cannot scrape and store."

    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"https://{url}"

    try:
        # Run async crawl synchronously
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        if loop.is_running():
            # If the loop is already running (e.g. within an async framework), use a thread or task
            import nest_asyncio
            nest_asyncio.apply()
            result = loop.run_until_complete(crawl_and_index_website(url))
        else:
            result = loop.run_until_complete(crawl_and_index_website(url))
            
        if result.get("status") == "success":
            return (
                f"SUCCESS: Crawled '{result.get('title')}' ({url}). "
                f"Split into {result.get('chunks_count')} chunks and saved to Pinecone."
            )
        else:
            return f"FAILED to crawl {url}: {result.get('message')}"

    except Exception as e:
        # Try running it using standard asyncio run as a fallback
        try:
            result = asyncio.run(crawl_and_index_website(url))
            if result.get("status") == "success":
                return (
                    f"SUCCESS: Crawled '{result.get('title')}' ({url}). "
                    f"Split into {result.get('chunks_count')} chunks and saved to Pinecone."
                )
            else:
                return f"FAILED to crawl {url}: {result.get('message')}"
        except Exception as ex:
            return f"Error executing scraper bot: {ex} (original error: {e})"
