import requests
import re
from bs4 import BeautifulSoup

import pdfkit
config = pdfkit.configuration(wkhtmltopdf = r"D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")


'''
	用几行代码把网上廖雪峰的Python教程在线教程爬下来转换成PDF文件，离线阅读

项目分析：
对网站的源码分析提取我们所要的价值性数据
	正文：<div class="x-wiki-content">...</div>
	导航条：<ul class="uk-nav uk-nav-side">...</ul>
	我们将导航条的url解析出来

'''


def get_html(url):
	try:
		r = requests.get(url, timeout = 30)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return

def get_url_list(html):
	soup = BeautifulSoup(html, 'html.parser')
	menu = soup.find_all(class_ = 'uk-nav uk-nav-side')[1]
	urls = []
	for li in menu.find_all('li'):
		url = 'http://www.liaoxuefeng.com' + li.a['href']
		urls.append(url)
	return urls

def get_content(url):
	html = get_html(url)
	soup = BeautifulSoup(html, 'html.parser')
	content = soup.find_all(class_ = 'x-wiki-content')[0]
	with open('Tutorial.html', 'a',encoding = 'utf-8') as f:
		f.write(str(content))

def save_pdf(htmls, file_name):
	options = {
		'page-size': 'Letter',
		'encoding': "UTF-8",
		'custom-header': [
			('Accept-Encoding', 'gzip')
		]
	}
	pdfkit.from_file(htmls, file_name, options = options, configuration = config)

def main():
	python_tutorial_url = 'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000#0'
	html = get_html(python_tutorial_url)
	urls = get_url_list(html)
	for url in urls:
		get_content(url)
	
	# get_content(python_tutorial_url)
	# save_pdf('Tutorial.html','Tutorial.pdf')

if __name__ == '__main__':
	main()