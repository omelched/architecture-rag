from pydantic_settings import CliApp
from .cli import RagSettings


if __name__ == "__main__":
    CliApp.run(RagSettings)
