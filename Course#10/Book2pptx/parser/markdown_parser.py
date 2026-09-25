# parser/markdown_parser.py

import re
from models.presentation_spec import (SlideSpec, PresentationSpec)

class MarkdownParser:

    def __init__(self):
        self.presentation_title = ""
        self.slides = []
        self.current_slide = None


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

            for line in f:
                line = line.strip()
                if not line:
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
