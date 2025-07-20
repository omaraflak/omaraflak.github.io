import bs4
import datetime
import article_pb2


TEMPLATE = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <link rel="stylesheet" href="../styles/index.css">
    <link rel="stylesheet" href="../styles/fonts.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
</head>

<body>
    <div id="header"></div>
    <div class="article-header">
        <div class="article-header-content">
            <h1 class="article-title">{{title}}</h1>
            <p class="article-description">{{description}}</p>
            <p class="article-date">{{date}}</p>
        </div>
    </div>
    <main class="article-main">
        <article class="article-body">
            {{content}}
        </article>
    </main>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
    <script src="../scripts/common.js"></script>
</body>

</html>
"""


def format_date(date: article_pb2.Date) -> str:
    time = datetime.datetime(date.year, date.month, date.day)
    return time.strftime('%b %d, %Y')


def format_content(contents: list[article_pb2.Content]) -> str:
    all_content = []
    for content in contents:
        if content.HasField('section'):
            all_content.append(
                f'<h2 class="article-section">{content.section}</h2>')
        if content.HasField('small_section'):
            all_content.append(
                f'<h3 class="article-small-section">{content.small_section}</h3>')
        if content.HasField('paragraph'):
            all_content.append(
                f'<p class="article-paragraph">{content.paragraph}</p>')
        if content.HasField('quote'):
            all_content.append(f'<p class="article-quote">{content.quote}</p>')
    return "\n".join(all_content)


def compile(article: article_pb2) -> str:
    html = TEMPLATE.replace("{{title}}", article.title)
    html = html.replace("{{description}}", article.description)
    html = html.replace("{{date}}", format_date(article.date))
    html = html.replace("{{content}}", format_content(article.contents))
    html = html.strip()
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup.prettify()
