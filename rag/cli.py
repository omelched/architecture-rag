import logging
import os

from pydantic_settings import BaseSettings, CliApp, CliSubCommand

from rag.bot import BotSubcommand
from rag.chat import ChatSubcommand
from rag.knowledge_management import QueryTestSubcommand, ReindexStoreSubcommand
from rag.scrape_wiki import ScrapeWikiSubcommand
from rag.test import TestSubcommand

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class RagSettings(
    BaseSettings, env_file=".env", env_prefix="RAG__", env_nested_delimiter="__"
):
    scrape_wiki: CliSubCommand[ScrapeWikiSubcommand]
    reindex: CliSubCommand[ReindexStoreSubcommand]
    query: CliSubCommand[QueryTestSubcommand]
    chat: CliSubCommand[ChatSubcommand]
    bot: CliSubCommand[BotSubcommand]
    test: CliSubCommand[TestSubcommand]

    yc_api_key: str

    def cli_cmd(self) -> None:
        os.environ["YC_API_KEY"] = self.yc_api_key
        CliApp.run_subcommand(self)
