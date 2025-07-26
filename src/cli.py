import os
import fire
import renderer


def generate(markdown_input_dir: str, html_output_dir: str):
    files = [file for file in os.listdir(
        markdown_input_dir) if file.endswith(".md")]

    entries = []

    for file in files:
        input_path = os.path.join(markdown_input_dir, file)
        filename = file.replace(".md", ".html")
        output_path = os.path.join(html_output_dir, filename)

        with open(input_path, "r") as fin:
            markdown = fin.read()
            if filename != "demo.html":
                entries.append(renderer.make_article_entry(markdown, filename))

            with open(output_path, "w") as fout:
                html = renderer.make_article(markdown)
                fout.write(html)

        print(input_path, "->", output_path)

    entries_html = "\n".join(entries)
    entries_path = os.path.join(html_output_dir, "all.html")
    with open(entries_path, "w") as fout:
        fout.write(entries_html)

    print(entries_path)


if __name__ == "__main__":
    fire.Fire(generate)
