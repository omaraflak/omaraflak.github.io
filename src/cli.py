import os
import fire
import renderer
import metadata
import sitemap


def generate(markdown_input_dir: str, html_output_dir: str, only: str | None = None):
    files = [
        file
        for file in os.listdir(markdown_input_dir)
        if file.endswith(".md")
    ]

    entries: list[tuple[str, metadata.Metadata]] = []
    sitemap_entries: list[str] = []

    for file in files:
        input_path = os.path.join(markdown_input_dir, file)
        filename = file.replace(".md", ".html")
        output_path = os.path.join(html_output_dir, filename)

        with open(input_path, "r") as fin:
            markdown = fin.read()
            if filename != "demo.html":
                meta = metadata.parse_metadata(markdown)
                entry = renderer.make_article_entry(meta, filename)
                entries.append((entry, meta))
                sitemap_entries.append(
                    sitemap.make_sitemap_entry(meta, filename))

            if not only or file == only:
                with open(output_path, "w") as fout:
                    html = renderer.make_article(markdown)
                    fout.write(html)

        if not only or file == only:
            print(">", output_path)

    entries.sort(key=lambda x: (x[1].pinned, x[1].date), reverse=True)
    entries = [entry for entry, _ in entries]
    entries_html = "\n".join(entries)
    entries_path = os.path.join(html_output_dir, "all.html")
    with open(entries_path, "w") as fout:
        fout.write(entries_html)
    print(">", entries_path)

    with open("public/sitemap.xml", "w") as fout:
        fout.write(sitemap.make_sitemap("\n".join(sitemap_entries)))
    print("> public/sitemap.xml")


if __name__ == "__main__":
    fire.Fire(generate)
