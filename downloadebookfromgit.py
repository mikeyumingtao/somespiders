# _*_ coding=utf-8 _*_
"""
爬取每个详情页面的pdf链接并存储在一个txt文件中
"""

import re
from time import sleep
# unquote用于解码中文字符
from urllib.parse import unquote

from bs4 import BeautifulSoup

from headers import headers
from LoginedReq import reqObject


def search_ebook(req, page, file):
	"""
	找到每个搜索结果每个页面详情页的链接，并存储在detail_page_link中
	"""
	params = {
		"p": page,
		"q": "电子书",
		"type": "Repositories"
	}
	reqs = req.get("https://github.com/search", params=params, headers=headers, verify=False)
	reb = BeautifulSoup(reqs.text, "lxml")
	for a in reb.find_all('a', attrs={"class": "v-align-middle"}):
		gol = a.get("href")
		try:
			get_into_detail_page_get_respositories(req, gol, gol, file)
		except ValueError:
			pass


def get_into_detail_page_get_respositories(req, gol, link, file):
	"""
	进入搜索结果的某一个结果页面，找到文件夹的链接并存储在链表中。
	"""
	pattern = re.compile('href="({link}.*?/tree/master/.*?)"'.format(link=link))
	url = "https://github.com" + link
	page_html_detail = req.get(url=url, headers=headers, verify=False)
	# 匹配每个详情页中的pdf链接，储存
	get_pdf_docs_link(page_html_detail, file, gol)
	hrefs = re.findall(pattern, page_html_detail.text)
	if hrefs:
		for href in hrefs:
			try:
				# 自我迭代，知道找到没有包的页面然后返回
				get_into_detail_page_get_respositories(req, gol, href, file)
			except Exception as e:
				print(e)
	else:
		try:
			resphtml = BeautifulSoup(page_html_detail, 'lxml')
			print([a.get('href') for a in resphtml.find_all('a', href=re.compile('.*?"'))])
		except Exception:
			raise ValueError


def get_pdf_docs_link(resp, file, link):
	"""
	找到每个respository中pdf的链接
	"""
	pattern = re.compile('href="({link}.*?pdf)"'.format(link=link))
	f = resp.text
	pdf_hrefs = re.findall(pattern, resp.text)
	if pdf_hrefs:
		print(pdf_hrefs)
		for df_href in pdf_hrefs:
			pdf_href = unquote(df_href)
			down_pdf_href = 'https://raw.githubusercontent.com' + pdf_href.replace('/blob', '')
			file.write(down_pdf_href)
			file.write('\n\n')
			file.flush()  # 立刻刷新缓冲区，这个在debug时可以立刻看到链接有没有写进文件中。


def write_to_file(path):
	"""
	给定一个文件路径，将抓取到的pdf文件链接放在该文件中
	:param path:
	:return:
	"""
	with open(path, 'a', encoding='utf-8') as file:
		for page in range(1, 3):
			try:
				search_ebook(reqObject, page, file)
				sleep(1)
			except Exception as e:
				print(e)
				continue


if __name__ == "__main__":
	write_to_file('githubpdflinks.txt')











