# RAG

## Установка

1. `python3.12 -m venv .venv`
2. `source .venv/bin/activate`
3. `python -m pip install -e .`

## Команды

### Наполнение базы знаний

`python -m rag scrape_wiki`

### Наполнение векторной БД

`python -m rag reindex`

#### Проверка поиска в индексе

```
usage: python -m rag query [-h] [--doc_count int] QUERY

positional arguments:
  QUERY

options:
  -h, --help       show this help message and exit
  --doc_count int  (default: 5)
```
