import urllib.request
from bs4 import BeautifulSoup

target_url = 'http://52.68.130.249/textboard/'

# 게시글의 제목과 목록을 가져오는 함수
def fetch_post_list():				
    URL = target_url
    res = urllib.request.urlopen(URL)
    html = res.read()

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='kingkongboard-table')

    title_list = table.find_all('td', class_='kingkongboard-list-title')

    links = []
    links = [td.find('a')['href'] for td in title_list]

    return links

result = fetch_post_list( )
print(result)

# 게시글의 세부 내역을  가져오는 함수
def fetch_post_contents(link) :
    URL = link
    res = urllib.request.urlopen(URL)
    html = res.read( )
    soup = BeautifulSoup(html,'html.parser')
    content_table = soup.find('div',id='kingkongboard-read-table')
    
    # 글제목 , 등록 날짜 가져오는 부분
    title_section = content_table.find('div',class_='title-section')
    title = title_section.find('h1').text
    date = title_section.find('div',class_='regist-date').find('h2').text

    # 글쓴이 정보를 가져오는 부분
    writer = content_table.find('div',class_='regist-writer').find('h2').text

    # 콘텐츠를 가져오는 부분
    content = content_table.find('div', class_='content-section').find('p').text

    # 결과를 모아서 출력하는 부분
    return {
         'title' : title,
         'date' : date,
         'writer' : writer,
         'content' : content
         }

 # 실제 결과를 출력하는 부분
links =fetch_post_list( )
for link in links :
     result = fetch_post_contents(link)
     print(result) 