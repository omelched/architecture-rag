import asyncio

import httpx
from bs4 import BeautifulSoup
from pydantic_settings import BaseSettings

from .knowledge_management import add_article

BASE_URL = "https://deathstranding.fandom.com"
INDEX_URL = "/ru/wiki/%D0%98%D0%BD%D1%82%D0%B5%D1%80%D0%B2%D1%8C%D1%8E"
INDEX_LINK_SELECTOR = "div.mw-content-ltr ul a"
MOCK_DICTIONARY = {
    "Хартмэн": "Сердцемэн",
    "Дайхардмэн": "ФСБмэн",
    "Дедмэн": "Франкенмэн",
    "Фрэджайл": "Хрупкайл",
    "Бриджес": "Мостикс",
    "Хиггс": "Пикс",
}


class ScrapeWikiSubcommand(BaseSettings):
    async def cli_cmd(self) -> None:
        await scrape_wiki()


async def fetch_page(url):
    async with httpx.AsyncClient() as client:
        page = await client.get(url)

    return page.content


async def scrape_article(article_url) -> tuple[str, str, str, str, str]:
    article_content = await fetch_page(BASE_URL + article_url)
    soup = BeautifulSoup(article_content, "html.parser")

    article_name = soup.select_one('h2[data-source="название"]').get_text()
    author = soup.select_one('div[data-source="объект"]').get_text().split("\n")[2]
    create_date = soup.select_one('div[data-source="время"]').get_text().split("\n")[2]
    place = soup.select_one('div[data-source="место"]').get_text().split("\n")[2]
    content = ""
    for paragraph in soup.select(".mw-body-content p")[2:]:
        content += paragraph.get_text() + "\n\n"

    for old_name, new_name in MOCK_DICTIONARY.items():
        article_name = article_name.replace(old_name, new_name)
        author = author.replace(old_name, new_name)
        place = place.replace(old_name, new_name)
        content = content.replace(old_name, new_name)

    return article_name, author, create_date, place, content


async def scrape_index():
    index_content = await fetch_page(BASE_URL + INDEX_URL)
    soup = BeautifulSoup(index_content, "html.parser")

    article_links = []
    for link in soup.select(INDEX_LINK_SELECTOR):
        if not link.attrs.get("href", "").startswith("/"):
            continue

        article_links.append(link.attrs["href"])

    return article_links


async def scrape_wiki():
    links = await scrape_index()

    for link in links:
        _, article_data = await asyncio.gather(asyncio.sleep(0.1), scrape_article(link))
        add_article(*article_data)
