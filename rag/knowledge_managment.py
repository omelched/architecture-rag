ARTICLE_PATTERN = """
---
author: %(author)s
create_date: %(create_date)s
place: %(place)s
---

# %(article_name)s


%(content)s

"""


def add_article(article_name, author, create_date, place, content):
    md_file_content = ARTICLE_PATTERN % {
        "article_name": article_name,
        "author": author,
        "create_date": create_date,
        "place": place,
        "content": content,
    }

    with open(f"./knowledge_base/{article_name}.md", "w", encoding="utf-8") as f:
        f.write(md_file_content)


if __name__ == "__main__":
    add_article(
        input("Название статьи: "),
        input("Автор: "),
        input("Дата: "),
        input("Место: "),
        input("Текст: "),
    )
