from pdf2docx import Converter

pdf_file = 'ใบแต่งทนาย.pdf'
docx_file = 'sample.docx'

# convert pdf to docx
cv = Converter(pdf_file)
cv.convert(docx_file)      # all pages by default
cv.close()