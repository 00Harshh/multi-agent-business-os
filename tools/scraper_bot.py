"""
Scraper Bot using Crawl4AI to scrape web pages, chunk them,
generate embeddings via Gemini, and save to Pinecone.
"""
import asyncio
import re
from typing import List, Dict, Any
import google.generativeai as genai
from pinecone import Pinecone, ServerlessSpec
from business_os.config.settings import settings

# Configure Gemini for Embeddings
if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)


def get_pinecone_index():
    """Retrieve or create the Pinecone index."""
    if not settings.pinecone_api_key:
        raise ValueError("PINECONE_API_KEY is not configured in settings or .env file.")

    pc = Pinecone(api_key=settings.pinecone_api_key)
    index_name = settings.pinecone_index_name or "business-os-knowledge"

    # List indexes and check if index exists
    try:
        existing_indexes = [idx.name for idx in pc.list_indexes()]
    except Exception as e:
        print(f"Error listing Pinecone indexes: {e}")
        existing_indexes = []

    # Recreate index if dimension mismatch (since gemini-embedding-001 is 3072-dimensional)
    if index_name in existing_indexes:
        try:
            desc = pc.describe_index(index_name)
            if desc.dimension != 3072:
                print(f"Pinecone index dimension mismatch ({desc.dimension} vs 3072). Recreating index...")
                pc.delete_index(index_name)
                # Wait for deletion
                import time
                while index_name in [idx.name for idx in pc.list_indexes()]:
                    time.sleep(1)
                existing_indexes.remove(index_name)
        except Exception as e:
            print(f"Error describing/deleting Pinecone index: {e}")

    if index_name not in existing_indexes:
        print(f"Index '{index_name}' not found. Creating serverless Pinecone index...")
        try:
            pc.create_index(
                name=index_name,
                dimension=3072,  # gemini-embedding-001 is 3072-dimensional
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            # Wait for index to be initialized
            import time
            while not pc.describe_index(index_name).status['ready']:
                time.sleep(1)
            print("Pinecone index created successfully!")
        except Exception as e:
            print(f"Error creating Pinecone index: {e}")
            raise e

    return pc.Index(index_name)


def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 150) -> List[str]:
    """Split text into overlapping semantic chunks of roughly chunk_size characters."""
    if not text:
        return []

    # Clean up excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Simple semantic splitting by paragraphs or sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if current_length + len(sentence) > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            # Implement overlap by keeping the last sentence if appropriate
            if len(current_chunk) > 1 and len(current_chunk[-1]) < chunk_overlap:
                current_chunk = [current_chunk[-1], sentence]
                current_length = len(current_chunk[0]) + len(sentence) + 1
            else:
                current_chunk = [sentence]
                current_length = len(sentence)
        else:
            current_chunk.append(sentence)
            current_length += len(sentence) + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def get_embedding(text: str) -> List[float]:
    """Generate text embeddings using Google's gemini-embedding-001 model."""
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not configured. Required for embeddings.")

    response = genai.embed_content(
        model="models/gemini-embedding-001",
        content=text,
        task_type="retrieval_document"
    )
    return response['embedding']


async def crawl_and_index_website(url: str) -> Dict[str, Any]:
    """Scrape a website using Crawl4AI, chunk the text, embed it, and save to Pinecone."""
    print(f"Starting Crawl4AI scraper on: {url}")
    try:
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
    except ImportError:
        # Fallback if crawl4ai is not installed/setup properly yet
        print("Crawl4AI not installed yet, simulating scrape...")
        return {"status": "error", "message": "Crawl4AI is not installed yet."}

    # Configure Crawl4AI run parameters
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        word_count_threshold=10,
        exclude_external_links=True
    )

    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=config)

            if not result.success:
                return {
                    "status": "error",
                    "message": f"Crawl failed: {result.error_message}"
                }

            # Retrieve clean markdown content
            markdown_content = result.markdown or ""
            title = result.metadata.get("title", "Unknown Page") if result.metadata else "Unknown Page"

            if not markdown_content.strip():
                return {
                    "status": "error",
                    "message": "Crawl completed, but no readable text content was found."
                }

            print(f"Crawl successful. Length: {len(markdown_content)} characters. Title: {title}")

            # Chunk content
            chunks = chunk_text(markdown_content)
            print(f"Split content into {len(chunks)} chunks.")

            # Get Pinecone index
            index = get_pinecone_index()

            # Process chunks and upsert to Pinecone
            vectors_to_upsert = []
            for i, chunk in enumerate(chunks):
                print(f"Embedding chunk {i+1}/{len(chunks)}...")
                embedding = get_embedding(chunk)
                
                # Make unique ID
                chunk_id = f"{re.sub(r'[^a-zA-Z0-9]', '_', url)}_{i}"
                
                vectors_to_upsert.append((
                    chunk_id,
                    embedding,
                    {
                        "url": url,
                        "title": title,
                        "chunk_index": i,
                        "content": chunk
                    }
                ))

            # Batch upsert to Pinecone (max 100 at a time)
            batch_size = 100
            for k in range(0, len(vectors_to_upsert), batch_size):
                batch = vectors_to_upsert[k:k+batch_size]
                index.upsert(vectors=batch)

            print(f"Successfully upserted {len(vectors_to_upsert)} chunks to Pinecone.")
            return {
                "status": "success",
                "url": url,
                "title": title,
                "chunks_count": len(chunks),
                "message": f"Successfully scraped, chunked, and indexed '{title}' to Pinecone."
            }

    except Exception as e:
        print(f"Exception during crawl_and_index_website: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
