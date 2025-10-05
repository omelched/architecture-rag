from pydantic_settings import BaseSettings, CliApp, CliSubCommand

from rag.knowledge_management import QueryTestSubcommand, ReindexStoreSubcommand
from rag.scrape_wiki import ScrapeWikiSubcommand


class RagSettings(BaseSettings):
    scrape_wiki: CliSubCommand[ScrapeWikiSubcommand]
    reindex: CliSubCommand[ReindexStoreSubcommand]
    query: CliSubCommand[QueryTestSubcommand]

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)
