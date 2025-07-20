import os
import fire
import parser
import compiler


class Cli:
    def generate_one(self, md_input: str, html_output: str):
        with open(md_input, "r") as fin:
            md = fin.read()
            article = parser.parse(md)
            with open(html_output, "w") as fout:
                html = compiler.compile(article)
                fout.write(html)

    def generate_many(self, md_inputs: str, html_outputs: str):
        files = [file for file in os.listdir(
            md_inputs) if file.endswith(".md")]
        for file in files:
            input_path = os.path.join(md_inputs, file)
            output_path = os.path.join(
                html_outputs, file.replace(".md", ".html"))
            print(input_path, "->", output_path)
            self.generate_one(input_path, output_path)


if __name__ == "__main__":
    fire.Fire(Cli)
