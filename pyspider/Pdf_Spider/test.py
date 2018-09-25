import pdfkit
config = pdfkit.configuration(wkhtmltopdf = r"D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
pdfkit.from_url("http://www.baidu.com", "out.pdf",configuration = config)