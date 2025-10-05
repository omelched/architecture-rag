import json
import logging

import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic_settings import BaseSettings

from rag import chat
from rag.knowledge_management import EMBEDDINGS_MODEL

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler("./test_log.log"))


def cosine_similarity_numpy(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0  # Handle cases where one or both vectors are zero vectors
    return dot_product / (norm_vec1 * norm_vec2)


class TestSubcommand(BaseSettings):
    async def cli_cmd(self) -> None:
        await test()


async def test():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)

    with open("golden_questions.json") as f:
        golden_questions = json.load(f)

    for question in golden_questions:
        response = await chat.chat(question["q"])

        result = cosine_similarity_numpy(
            embeddings.embed_query(response),
            embeddings.embed_query(question["a"]),
        )
        test_result_log = {"test_question": question["q"], "similarity": result}
        logger.info(f"{test_result_log}")
