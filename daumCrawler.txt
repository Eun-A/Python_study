from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import os

apikey = "48c388bf9a994b61d9d2a061cc29aee9"
default_url = "https://apis.daum.net/search/web?output=xml&apikey="

def get_save_path():
	save_path = str(input("저장할 위치와 파일명을 적어주세요. : "))
	save_path = save_path.replace("\\", "/")

	if not os.path.isdir(os.path.split(save_path)[0]):
		os.mkdir(os.path.split(save_path)[0])

	return save_path

def get_result_xml():
	search = str(input("검색할 문장을 입력하세요: "))
	search = urllib.parse.quote(search)

	full_url = default_url + apikey + '&q=' + search
	res = urllib.request.urlopen(full_url).read()

	return res

def fetch_result_xml():
	result_xml = get_result_xml()
	bs = BeautifulSoup(result_xml, 'html.parser')
	
	items = bs.find_all("item")

	f = open(get_save_path(), 'w', encoding = 'utf-8')

	for item in items:
		date = item.find("pubdate").get_text(strip=True)
		title = item.find("title").get_text(strip=True)
		desc = item.find("description").get_text(strip=True)
		link = item.find("link").get_text(strip=True)
		url = item.find("url").get_text(strip=True)

		f.write("==" * 30 + '\n')
		f.write("게시물 날짜 : " + date + '\n')
		f.write("제목 : " + title + '\n')
		f.write("설명 : " + desc + '\n')
		f.write("링크 : " + link + '\n')
		f.write("URL : " + url + '\n')

		f.write("==" * 30 + '\n')


fetch_result_xml()