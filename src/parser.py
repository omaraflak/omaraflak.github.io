import re
import article_pb2

METADATA_PATTERN = r"^:(.+):(.+)$"


def parse(data: str) -> article_pb2.Article:
    lines = [line for line in data.splitlines() if line !=
             "" and not line.isspace()]

    article = article_pb2.Article()
    for line in lines:
        metadata = re.findall(METADATA_PATTERN, line)
        if metadata:
            key, value = metadata[0]
            value = value.strip()

            if key == "title":
                article.title = value
            elif key == "description":
                article.description = value
            elif key == "year":
                article.date.year = int(value)
            elif key == "month":
                article.date.month = int(value)
            elif key == "day":
                article.date.day = int(value)

            continue

        content = article_pb2.Content()
        if line.startswith("#"):
            content.section = line.strip("#").strip()
        elif line.startswith("##"):
            content.small_section = line.strip("#").strip()
        elif line.startswith(">"):
            content.quote = line.strip(">").strip()
        else:
            content.paragraph = line.strip()
        article.contents.append(content)

    return article
