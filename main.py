import json
import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()


async def fetch_titles(session, page):
    url = f"https://habr.com/ru/search/page{page}/?q=python&target_type=posts&order=relevance"
    html = await fetch_html(session, url)
    soup = BeautifulSoup(html, "html.parser")
    titles = [text.text for text in soup.findAll("h2", class_="tm-title tm-title_h2")]
    return titles


async def main():
    habr_titles_list = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_titles(session, i) for i in range(1, 6)]
        results = await asyncio.gather(*tasks)
        for titles in results:
            habr_titles_list.extend(titles)

    with open("asyncio/titles.json", "w", encoding="utf-8") as file:
        json.dump(habr_titles_list, file, indent=4, ensure_ascii=False)


# Run the asyncio event loop
asyncio.run(main())
