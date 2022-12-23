from pdf2docx import Converter

pdf = 'test_file.pdf'

docx = 'mynew.docx'

cv=Converter(pdf)

cv.convert(docx)