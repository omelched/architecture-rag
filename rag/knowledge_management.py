import os
import time

import yaml
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic_settings import BaseSettings, CliPositionalArg

ARTICLE_PATTERN = """---
author: %(author)s
create_date: %(create_date)s
place: %(place)s
---

# %(article_name)s

%(content)s
"""
EMBEDDINGS_MODEL = "all-MiniLM-L6-v2"
KNOWLEDGE_BASE_DIR = "./knowledge_base"
CHROMADB_DIR = "./chroma-data"


class ReindexStoreSubcommand(BaseSettings):
    async def cli_cmd(self) -> None:
        started = time.time()
        await reindex_vector_store()
        print(f"Индексация заняла {time.time() - started:.4f} секунд.")


class QueryTestSubcommand(BaseSettings):
    query: CliPositionalArg[str]
    doc_count: int = 5

    async def cli_cmd(self) -> None:
        articles = await query_top_articles(self.query, count=self.doc_count)
        for article, score in articles:
            print("Score:", score, "\t", article.page_content, "\n---")


def load_markdown_with_metadata(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    content_parts = content.split("---", 2)

    if len(content_parts) == 3:
        _, yaml_metadata, body = content_parts
        try:
            metadata = yaml.safe_load(yaml_metadata) or {}
        except yaml.YAMLError:
            metadata = {}
    else:
        body = content
        metadata = {}

    filtered_body = ""
    for line in body.splitlines():
        if line.startswith("#"):
            continue
        stripped_line = line.strip()
        if stripped_line:
            filtered_body += stripped_line + "\n"

    metadata["source"] = os.path.basename(file_path)

    return Document(page_content=filtered_body, metadata=metadata)


async def reindex_vector_store():
    docs = []
    for root, _, files in os.walk(KNOWLEDGE_BASE_DIR):
        for file in files:
            if not file.endswith(".md"):
                continue

            path = os.path.join(root, file)
            docs.append(load_markdown_with_metadata(path))
    print(f"Loaded {len(docs)} markdown documents with metadata.")

    splitter = RecursiveCharacterTextSplitter(
        separators="markdown",
        chunk_size=256,
        chunk_overlap=64,
    )
    splitted_docs = splitter.split_documents(docs)
    print(f"Split into {len(splitted_docs)} chunks total.")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)
    await Chroma.afrom_documents(
        documents=splitted_docs,
        embedding=embeddings,
        persist_directory=f"{CHROMADB_DIR}",
    )
    print(f"✅ Vector store created and saved to '{CHROMADB_DIR}'")


async def query_top_articles(query, count: int):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)
    vectorstore = Chroma(
        persist_directory=CHROMADB_DIR,
        embedding_function=embeddings,
    )

    results = await vectorstore.asimilarity_search_with_relevance_scores(query, k=count)

    return results


def add_article(article_name, author, create_date, place, content):
    md_file_content = ARTICLE_PATTERN % {
        "article_name": article_name,
        "author": author,
        "create_date": create_date,
        "place": place,
        "content": content,
    }

    with open(f"{KNOWLEDGE_BASE_DIR}/{article_name}.md", "w", encoding="utf-8") as f:
        f.write(md_file_content)
