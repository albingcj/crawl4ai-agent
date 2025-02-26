import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
import re

# def clean_markdown(text):
#     # Remove Markdown images (e.g., ![alt text](URL))
#     text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

#     # Remove Markdown links (e.g., [anchor text](URL))
#     text = re.sub(r'\[.*?\]\(.*?\)', '', text)

#     # Remove asterisks often used for bullets or emphasis
#     text = text.replace('*', '')

#     # Remove Markdown heading markers like ## or ###
#     text = re.sub(r'#+\s*', '', text)

#     # Replace multiple newlines with a single newline
#     text = re.sub(r'\n\s*\n+', '\n', text)

#     # Strip extra spaces from each line
#     lines = [line.strip() for line in text.split('\n')]

#     # Rejoin non-empty lines
#     cleaned_text = '\n'.join(line for line in lines if line)

#     return cleaned_text

# def clean_markdown(text):
#     # Remove Markdown images (e.g., ![alt text](URL))
#     text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

#     # Remove Markdown links (e.g., [anchor text](URL))
#     text = re.sub(r'\[.*?\]\(.*?\)', '', text)

#     # Remove asterisks often used for bullets or emphasis
#     text = text.replace('*', '')

#     # Replace multiple newlines with a single newline
#     text = re.sub(r'\n\s*\n+', '\n', text)

#     # Strip extra spaces from each line
#     lines = [line.strip() for line in text.split('\n')]

#     # Rejoin non-empty lines
#     cleaned_text = '\n'.join(line for line in lines if line)

#     return cleaned_text
import re


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


# def clean_markdown(text):
#     # Remove Markdown images but keep the ! (e.g., ![alt text](URL) -> !)
#     text = re.sub(r'!\[.*?\]\(.*?\)', '!', text)

#     # Remove Markdown links (e.g., [anchor text](URL))
#     text = re.sub(r'\[.*?\]\(.*?\)', '', text)

#     # Remove asterisks often used for bullets or emphasis
#     text = text.replace('*', '')

#     # Replace multiple newlines with a single newline
#     text = re.sub(r'\n\s*\n+', '\n', text)

#     # Strip extra spaces from each line
#     lines = [line.strip() for line in text.split('\n')]

#     # Rejoin non-empty lines
#     cleaned_text = '\n'.join(line for line in lines if line)

#     return cleaned_text

import os


async def main():
    browser_config = BrowserConfig(verbose=True)
    run_config = CrawlerRunConfig(
        # Content filtering
        word_count_threshold=100,
        exclude_external_links=True,
        only_text=True,
        # Cache control
        cache_mode=CacheMode.ENABLED,  # Use cache if available
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            # url="https://www.goldmansachs.com/our-firm/our-people-and-leadership/leadership",
            url="https://zeb.co",
            config=run_config,
        )
        out = "test"
        if result.success:
            # Print clean content
            # print("Content:", result.markdown)

            with open(os.path.join(out, "original_md.txt"), "w", encoding="utf-8") as f:
                f.write(result.markdown)

            with open(os.path.join(out, "cleaned_md.txt"), "w", encoding="utf-8") as f:
                f.write(clean_markdown(result.markdown))

            # print(clean_markdown(result.markdown))

            # # Process images
            # for image in result.media["images"]:
            #     print(f"Found image: {image['src']}")

            # # Process links
            # for link in result.links["internal"]:
            #     print(f"Internal link: {link['href']}")

        else:

            print(f"Crawl failed: {result.error_message}")


if __name__ == "__main__":
    asyncio.run(main())
