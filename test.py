# import asyncio
# import aiofiles  # For async file operations
# import re  # For regex-based markdown cleaning
# from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
# from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
# from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
# from crawl4ai.deep_crawling.filters import (
#     FilterChain,
#     DomainFilter,
#     URLPatternFilter,
#     ContentTypeFilter
# )
# from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer

# # Function to clean markdown content
# def clean_markdown(text):
#     # Remove Markdown images but keep the ! (e.g., ![alt text](URL) -> !)
#     text = re.sub(r"!\[.*?\]\(.*?\)", "!", text, flags=re.DOTALL)

#     # Remove Markdown links, even if the link text spans multiple lines (e.g., [text](URL) -> '')
#     text = re.sub(r"\[.*?\]\(.*?\)", "", text, flags=re.DOTALL)

#     # Remove stray URL patterns in angle brackets that might remain in malformed markdown (e.g., <http://example.com> -> '')
#     text = re.sub(r"<https?:\/\/[^>\s]+>", "", text)

#     # Remove asterisks often used for bullets or emphasis
#     text = text.replace("*", "")

#     # Replace multiple newlines with a single newline
#     text = re.sub(r"\n\s*\n+", "\n", text)

#     # Strip extra spaces from each line and rejoin non-empty lines
#     lines = [line.strip() for line in text.split("\n")]

#     # Consolidate consecutive '!' symbols into one per line
#     cleaned_text = []
#     for line in lines:
#         if line == "!":
#             if not cleaned_text or cleaned_text[-1] != "!":
#                 cleaned_text.append("!")
#         elif line:
#             cleaned_text.append(line)

#     # Rejoin the lines into cleaned text
#     cleaned_text = "\n".join(cleaned_text)

#     return cleaned_text

# async def run_advanced_crawler():
#     # Create a sophisticated filter chain
#     filter_chain = FilterChain([
#         # Domain boundaries
#         DomainFilter(
#             allowed_domains=["www.goldmansachs.com"],  # Adjusted to match your base URL
#             blocked_domains=[]
#         ),

#         # URL patterns to include
#         URLPatternFilter(patterns=["*leadership*", "*team*", "*about*", "*executive*"]),

#         # Content type filtering
#         ContentTypeFilter(allowed_types=["text/html"])
#     ])

#     # Create a relevance scorer focused on leadership keywords
#     keyword_scorer = KeywordRelevanceScorer(
#         keywords=["leadership", "executive", "ceo", "director", "manager", "team"],
#         weight=0.7
#     )

#     # Set up the configuration
#     config = CrawlerRunConfig(
#         deep_crawl_strategy=BestFirstCrawlingStrategy(
#             max_depth=5,
#             include_external=False,
#             filter_chain=filter_chain,
#             url_scorer=keyword_scorer
#         ),
#         scraping_strategy=LXMLWebScrapingStrategy(),
#         stream=True,
#         verbose=True
#     )

#     # Execute the crawl
#     results = []
#     visited_urls = []  # To store all visited URLs
#     async with AsyncWebCrawler() as crawler:
#         # Open file for writing (async) with UTF-8 encoding
#         async with aiofiles.open('crawled_markdown.txt', mode='w', encoding="utf-8") as f:
#             async for result in await crawler.arun("https://www.goldmansachs.com", config=config):
#                 results.append(result)
#                 score = result.metadata.get("score", 0)
#                 depth = result.metadata.get("depth", 0)
#                 visited_urls.append(result.url)  # Add URL to visited list

#                 # Print to console
#                 print(f"Depth: {depth} | Score: {score:.2f} | {result.url}")

#                 # Clean the markdown content
#                 cleaned_markdown = clean_markdown(result.markdown)

#                 # Write to file
#                 await f.write(f"{'=' * 40}\n")
#                 await f.write(f"URL: {result.url}\n")
#                 await f.write(f"Depth: {depth}\n")
#                 await f.write(f"Score: {score:.2f}\n")
#                 await f.write(f"Cleaned Markdown:\n{cleaned_markdown}\n\n")

#     # Save all visited URLs to a separate file
#     async with aiofiles.open('visited_urls.txt', mode='w', encoding="utf-8") as f:
#         await f.write("Visited URLs:\n")
#         await f.write("=========================\n")
#         for url in visited_urls:
#             await f.write(f"{url}\n")

#     print(f"Crawled {len(results)} high-value pages")
#     print(f"Average score: {sum(r.metadata.get('score', 0) for r in results) / len(results):.2f}")

#     # Group by depth
#     depth_counts = {}
#     for result in results:
#         depth = result.metadata.get("depth", 0)
#         depth_counts[depth] = depth_counts.get(depth, 0) + 1

#     print("Pages crawled by depth:")
#     for depth, count in sorted(depth_counts.items()):
#         print(f"  Depth {depth}: {count} pages")

# if __name__ == "__main__":
#     asyncio.run(run_advanced_crawler())

import asyncio
import aiofiles  # For async file operations
import re  # For regex-based markdown cleaning
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.filters import (
    FilterChain,
    DomainFilter,
    URLPatternFilter,
    ContentTypeFilter
)
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer

# Function to clean markdown content
def clean_markdown(text):
    # Remove Markdown images but keep the ! (e.g., ![alt text](URL) -> !)
    text = re.sub(r"!\[.*?\]\(.*?\)", "!", text, flags=re.DOTALL)

    # Remove Markdown links, even if the link text spans multiple lines (e.g., [text](URL) -> '')
    text = re.sub(r"\[.*?\]\(.*?\)", "", text, flags=re.DOTALL)

    # Remove stray URL patterns in angle brackets that might remain in malformed markdown (e.g., <http://example.com> -> '')
    text = re.sub(r"<https?:\/\/[^>\s]+>", "", text)

    # Remove asterisks often used for bullets or emphasis
    text = text.replace("*", "")

    # Replace multiple newlines with a single newline
    text = re.sub(r"\n\s*\n+", "\n", text)

    # Strip extra spaces from each line and rejoin non-empty lines
    lines = [line.strip() for line in text.split("\n")]

    # Consolidate consecutive '!' symbols into one per line
    cleaned_text = []
    for line in lines:
        if line == "!":
            if not cleaned_text or cleaned_text[-1] != "!":
                cleaned_text.append("!")
        elif line:
            cleaned_text.append(line)

    # Rejoin the lines into cleaned text
    cleaned_text = "\n".join(cleaned_text)

    return cleaned_text

async def run_advanced_crawler():
    # Create a sophisticated filter chain
    filter_chain = FilterChain([
        # Domain boundaries
        DomainFilter(
            allowed_domains=["zeb.co"],  # Adjusted to match your base URL
            blocked_domains=[]
        ),

        # URL patterns to include
        URLPatternFilter(patterns=["*product*", "*service*", "*solution*", "*business*"]),

        # Content type filtering
        ContentTypeFilter(allowed_types=["text/html"])
    ])

    # Create a relevance scorer focused on product/service/solution keywords
    keyword_scorer = KeywordRelevanceScorer(
        keywords=["product", "service", "solution", "business", "offering", "platform"],
        weight=0.7
    )

    # Set up the configuration
    config = CrawlerRunConfig(
        deep_crawl_strategy=BestFirstCrawlingStrategy(
            max_depth=2,
            include_external=False,
            filter_chain=filter_chain,
            url_scorer=keyword_scorer
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        stream=True,
        verbose=True
    )

    # Execute the crawl
    results = []
    visited_urls = []  # To store all visited URLs
    products_and_solutions = []  # To store extracted product/service/solution details
    async with AsyncWebCrawler() as crawler:
        # Open file for writing (async) with UTF-8 encoding
        async with aiofiles.open('crawled_markdown.txt', mode='w', encoding="utf-8") as f:
            async for result in await crawler.arun("https://zeb.co", config=config):
                results.append(result)
                score = result.metadata.get("score", 0)
                depth = result.metadata.get("depth", 0)
                visited_urls.append(result.url)  # Add URL to visited list

                # Print to console
                print(f"Depth: {depth} | Score: {score:.2f} | {result.url}")

                # Clean the markdown content
                cleaned_markdown = clean_markdown(result.markdown)

                # Write to file
                await f.write(f"{'=' * 40}\n")
                await f.write(f"URL: {result.url}\n")
                await f.write(f"Depth: {depth}\n")
                await f.write(f"Score: {score:.2f}\n")
                await f.write(f"Cleaned Markdown:\n{cleaned_markdown}\n\n")

                # Extract product/service/solution details
                lines = cleaned_markdown.split("\n")
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines

                    # Look for lines containing relevant keywords
                    if any(keyword in line.lower() for keyword in ["product", "service", "solution", "business"]):
                        products_and_solutions.append({
                            "url": result.url,
                            "detail": line
                        })

    # Save all visited URLs to a separate file
    async with aiofiles.open('visited_urls.txt', mode='w', encoding="utf-8") as f:
        await f.write("Visited URLs:\n")
        await f.write("=========================\n")
        for url in visited_urls:
            await f.write(f"{url}\n")

    # Save product/service/solution details to a separate file
    async with aiofiles.open('products_and_solutions.txt', mode='w', encoding="utf-8") as f:
        await f.write("Products, Services, and Solutions:\n")
        await f.write("=========================\n")
        for item in products_and_solutions:
            await f.write(f"URL: {item['url']}\n")
            await f.write(f"Detail: {item['detail']}\n")
            await f.write("-" * 40 + "\n")

    print(f"Crawled {len(results)} high-value pages")
    print(f"Average score: {sum(r.metadata.get('score', 0) for r in results) / len(results):.2f}")

    # Group by depth
    depth_counts = {}
    for result in results:
        depth = result.metadata.get("depth", 0)
        depth_counts[depth] = depth_counts.get(depth, 0) + 1

    print("Pages crawled by depth:")
    for depth, count in sorted(depth_counts.items()):
        print(f"  Depth {depth}: {count} pages")

if __name__ == "__main__":
    asyncio.run(run_advanced_crawler())