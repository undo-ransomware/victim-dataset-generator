import os
import pptx
from pptx.util import Inches, Pt
from PIL import Image
from resizeimage import resizeimage
from math import sqrt
from tempfile import mkstemp

class Presentation:
	def __init__(self):
		self.pptx = pptx.Presentation()
	
	def make_title(self, title, subtitle, *subsubtitles):
		slide = self.pptx.slides.add_slide(self.pptx.slide_layouts[0])
		slide.shapes.title.text = title
		textbox = slide.placeholders[1].text_frame
		textbox.text = subtitle
		textbox.paragraphs[0].font.size = Pt(28)
		for sst in subsubtitles:
			p = textbox.add_paragraph()
			p.text = sst
			p.font.size = Pt(16)

	def make_bulleted(self, title, bullets):
		slide = self.pptx.slides.add_slide(self.pptx.slide_layouts[1])
		slide.shapes.title.text = title
		textbox = slide.shapes.placeholders[1].text_frame
		textbox.text = "\n".join(bullets)
		# in classic bad presentation style, reduce font size until the text fits.
		# 240 is a rough estimate for how much text fits on one page at size 36.
		size = max(min(sqrt(200) / sqrt(len(textbox.text)) * 36, 36), 1)
		for p in textbox.paragraphs:
			p.font.size = Pt(size)

	def make_image(self, filename, caption):
		with Image.open(filename) as img:
			width, height = img.size

		# usable size is 5.5" x 8.0" in the idiotic-inch based default template.
		# in classic bad presentation style, we use most of that for the caption.
		WIDTH, HEIGHT, MARGIN = 8.0, 5.0, 1.0
		w = h = None
		x = y = Inches(MARGIN)
		if height / HEIGHT > width / WIDTH:
			h = Inches(HEIGHT)
			x = Inches((WIDTH - HEIGHT / height * width) / 2 + MARGIN)
		else:
			w = Inches(WIDTH)
			y = Inches((HEIGHT - WIDTH / width * height) / 2 + MARGIN)
		slide = self.pptx.slides.add_slide(self.pptx.slide_layouts[6])
		temp = mkstemp(suffix=os.path.splitext(filename)[1])[1]
		with Image.open(filename) as img:
			resizeimage.resize_thumbnail(img, [1200, 750]).save(temp)
		slide.shapes.add_picture(temp, x, y, width=w, height=h)
		os.remove(temp)

		x, y = Inches(MARGIN), Inches(HEIGHT + 1.2 * MARGIN)
		w, h = Inches(WIDTH), Inches(MARGIN)
		textbox = slide.shapes.add_textbox(x, y, w, h).text_frame
		textbox.text = caption
		# make the text fit. single-line, so roughly linear
		size = max(min(40.0 / len(textbox.text) * 36, 36), 1)
		for p in textbox.paragraphs:
			p.font.size = Pt(size)

	def save(self, filename):
		self.pptx.save(filename)
