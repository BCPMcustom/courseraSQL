# parser/markdown_parser.py

import re
from models.presentation_spec import (SlideSpec, PresentationSpec)
from html.parser import HTMLParser
from parser.html_table_renderer import HTMLTableRenderer
import matplotlib.pyplot as plt

class TableParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.rows = []
        self.current_row = []
        self.current_cell = ""
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag in ("th", "td"):
            self.in_cell = True
            self.current_cell = ""
        elif tag == "tr":
            self.current_row = []

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data

    def handle_endtag(self, tag):

        if tag in ("th", "td"):
            self.current_row.append(
                self.current_cell.strip()
            )
            self.in_cell = False

        elif tag == "tr":
            if self.current_row:
                self.rows.append(
                    self.current_row
                )

class HTMLTableRenderer:

    def __init__(self):
        self.table_count = 0

    def render(self, html_table):

        parser = TableParser()
        parser.feed(html_table)
        rows = parser.rows

        filename = (
            f"table_{self.table_count}.png"
        )

        self.table_count += 1

        fig, ax = plt.subplots()

        ax.axis("off")

        table = ax.table(
            cellText=rows,
            loc="center"
        )

        table.auto_set_font_size(False)
        table.set_fontsize(8)

        table.scale(1, 1.5)

        plt.savefig(
            filename,
            bbox_inches="tight",
            dpi=200
        )

        plt.close(fig)

        return filename

class MarkdownParser:

    def __init__(self):
        self.presentation_title = ""
        self.slides = []
        self.current_slide = None
        self.table_renderer = HTMLTableRenderer()


    def parse_heading(self, line):
        if line.startswith("# "):

            text = line[2:].strip()

            if self.presentation_title == "":
                self.presentation_title = text
            else:
                self.closing_title = text
            

        elif line.startswith("## "):
            title = line[3:].strip()
            print(f"NEW SLIDE: {title}")
            self.current_slide = SlideSpec(title)
            self.slides.append(self.current_slide)


        
    def parse_bullet(self, line):

        if line.startswith("- "):
            bullet = line[2:].strip()
            if self.current_slide:
                self.current_slide.bullets.append(bullet)


    def parse_image(self, line):

        IMAGE_RE = r'!\[(.*?)\]\((.*?)\)'

        match = re.search(IMAGE_RE, line)

        if (match and self.current_slide is not None):
            if match:
                filename = match.group(2)
                self.current_slide.images.append(filename)


    def parse_callouts(self, line):

        if line.startswith("#### "):
            text = line[5:].strip()
            self.current_slide.callouts.append(text)


        
    def parse(self, filename):

        with open(filename, encoding="utf-8") as f:

            in_table = False
            table_lines = []

            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                if in_table:
                    table_lines.append(line)
                    if "</table>" in line:
                        html_table = "\n".join(table_lines)
                        filename = (self.table_renderer.render(html_table))
                        image_line = (f"![table]({filename})")
                        self.parse_image(image_line)
                        table_lines = []
                        in_table = False
                    continue
                if "<table" in line:
                    in_table = True
                    table_lines = [line]
                    continue

                self.parse_heading(line)
                self.parse_bullet(line)
                self.parse_image(line)
                self.parse_callouts(line)

        return PresentationSpec(
            title=self.presentation_title,
            slides=self.slides,
            closing_title=self.closing_title
        )


###  Debug Section

parser = MarkdownParser()

presentation = parser.parse(
    "MintClassics.md"
)


print("\nPresentation Title:")
print(presentation.title)

print()
print("Closing Slide:")
print(presentation.closing_title)

for slide in presentation.slides:

    print()
    print(slide.title)

    print("Bullets:")

    for bullet in slide.bullets:
        print(f"  - {bullet}")

    print("Images:")

    for image in slide.images:
        print(f"  - {image}")

    print("Callouts:")

    for callout in slide.callouts:
        print(f"  - {callout}")

