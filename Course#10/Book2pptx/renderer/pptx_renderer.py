import os
from pptx import Presentation
from pptx.util import Inches



class PowerPointRenderer:
    def render(self, presentation_spec):
        prs = Presentation()
        title_slide_layout = prs.slide_layouts[0]
        slide_layout = prs.slide_layouts[1]                #This layout give title_bar at the top, and a multimedia box
        slide = prs.slides.add_slide(title_slide_layout)    
        title = slide.shapes.title
        title.text = presentation_spec.title

        raw_path = ""
        img_path = ""
        i = -1
        
        for slide in presentation_spec.slides:
            i += 1
            slide = prs.slides.add_slide(slide_layout)    
            title = slide.shapes.title
            title.text = presentation_spec.slides[i].title

        
            if presentation_spec.slides[i].images:

                img_count = 0
                image = presentation_spec.slides[i].images

                for image[img_count] in presentation_spec.slides[i].images:
                            
                    raw_path = presentation_spec.slides[i].images[img_count]
                    img_path = os.path.abspath(raw_path)         
                    print(f"\nThe image path for {i}", img_path)
                    print("\nThe image count is", img_count, "\n")
                    left = top = Inches(1)
                    pic = slide.shapes.add_picture(img_path, left, top)
                    img_count += 1



        slide = prs.slides.add_slide(title_slide_layout)    
        title = slide.shapes.title
        title.text = presentation_spec.closing_title

        prs.save('test.pptx')
        
