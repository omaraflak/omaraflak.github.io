ARTICLE = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="{{title}}">
    <meta property="og:description" content="{{description}}">
    <title>{{title}}</title>
    <link rel="icon" type="image/svg+xml" href="/images/favicon.svg">
    <link rel="stylesheet" href="../styles/index.css">
    <link rel="stylesheet" href="../styles/fonts.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css" integrity="sha512-fHwaWebuwA7NSF5Qg/af4UeDx9XqUpYpOGgubo3yWu+b2IQR4UeQwbb42Ti7gVAjNtVoI/I9TEoYeu9omwcC6g==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/styles/github.min.css" integrity="sha512-0aPQyyeZrWj9sCA46UlmWgKOP0mUipLQ6OZXu8l4IcAmD2u31EPEy9VcIMvl7SoAaKe8bLXZhYoMaE/in+gcgA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>

<body>
    <div class="site-header">
        <div class="site-header-content">
            <a href="/index.html" class="site-header-link">Home</a>
            <a href="/articles.html" class="site-header-link">Blog</a>
        </div>
    </div>
    <div class="article-header">
        <div class="article-header-content">
            <h1 class="article-title">{{title}}</h1>
            <p class="article-description">{{description}}</p>
            <p class="article-date">{{date}}</p>
            {{updated_date}}
        </div>
    </div>
    <main class="article-main">
        <article class="article-body">
            {{content}}
        </article>
    </main>
    <div class="article-hr"></div>
    <div class="site-footer">
        <div class="site-footer-content"></div>
    </div>
    <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js" integrity="sha512-LQNxIMR5rXv7o+b1l8+N1EZMfhG7iFZ9HhnbJkTp4zjNr5Wvst75AqUeFDxeRUa7l5vEDyUiAip//r+EFLLCyA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js" integrity="sha512-iWiuBS5nt6r60fCz26Nd0Zqe0nbk1ZTIQbl3Kv7kYsX+yKMUFHzjaH2+AnM6vp2Xs+gNmaBAVWJjSmuPw76Efg==" crossorigin="anonymous" referrerpolicy="no-referrer" onload="renderMathInElement(document.body, {
        delimiters: [
            {left: '[begin-latex]', right: '[end-latex]', display: true},
            {left: '[begin-latex-inline]', right: '[end-latex-inline]', display: false},
        ]
    });"></script>
    <script defer src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js" integrity="sha512-EBLzUL8XLl+va/zAsmXwS7Z2B1F9HUHkZwyS/VKwh3S7T/U0nF4BaU29EP/ZSf6zgiIxYAnKLu6bJ8dqpmX5uw==" crossorigin="anonymous" referrerpolicy="no-referrer" onload="hljs.highlightAll();"></script>
    <script defer src="https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/viz.js" integrity="sha512-vnRdmX8ZxbU+IhA2gLhZqXkX1neJISG10xy0iP0WauuClu3AIMknxyDjYHEpEhi8fTZPyOCWgqUCnEafDB/jVQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script defer src="https://cdnjs.cloudflare.com/ajax/libs/viz.js/2.1.2/lite.render.js" integrity="sha512-uAHj1knkgGpl0fJcyjbcVY0f9j252eWzEeBxE4s4AQkPJkp/+U+rlfoOXlwreSzPhndCT+5YR00/QSD/nPqb+g==" crossorigin="anonymous" referrerpolicy="no-referrer" onload="
        const viz = new Viz();
        document.querySelectorAll('.article-graphviz').forEach(element => {
            const content = element.textContent;
            try {
                viz.renderSVGElement(content)
                    .then(svg => {
                        element.textContent = '';
                        element.appendChild(svg);
                    })
                    .catch(error => {
                        console.error('Error rendering Graphviz SVG:', error);
                        element.textContent = 'Error rendering graph. Check console for details.';
                    });
            } catch (error) {
                console.error('Error with Viz.js rendering process:', error);
                element.textContent = 'Error during graph rendering setup.';
            }
        });
    "></script>
</body>

</html>
"""

UPDATED_DATE = """<span class="article-updated-date">Updated on {{date}}</span>"""

ENTRY = """
<article class="articles-preview">
    <div class="articles-preview-title-container">
        <a href="articles/{{filename}}" class="articles-preview-title">{{title}}</a>
        {{pin}}
    </div>
    <p class="articles-preview-date">{{date}}</p>
    <p class="articles-preview-description">{{description}}</p>
</article>
"""

PIN = """<img src="/images/pin.svg" class="articles-preview-pin"></img>"""
