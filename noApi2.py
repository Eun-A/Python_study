# Open API 가 없는 사이트용 크롤러- 전체 완성코드(댓글 및 파일저장기능포함)

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

    # 이미지를 가져오는 부분
    image = content_table.find('div',class_='content-section').find('img')
    image_url = ''
    if image :
        image_url = image['src']

    # 댓글을 가져오는 부분
    comments = [ ]
    comment_section = content_table.find('div',class_='comment-section')
    list_wrapper = comment_section.find('div',class_='list-wrapper')
    comment_list = list_wrapper.find_all('div',class_='each-comment')
    if comment_list :
        for comment in comment_list :
            comment_box = comment.find('div',class_='comment-box')
            comment_content = comment_box.find('div',class_='comment-content')

            div_writer = comment_content.find('div',class_='comment-content-writer')
            writer = div_writer.find('span',class_='author').text
            date = div_writer.find('span',class_='date').text

            div_text = comment_content.find('div',class_='comment-content-text')
            comment_text = div_text.find('h2').text

            comments.append( {
                'writer' : writer ,
                'date' : date ,
                'comment_text' : comment_text
                } )

    # 결과를 모아서 출력하는 부분
    return {
         'title' : title,
         'date' : date,
         'writer' : writer,
         'content' : content,
         'image' : image_url ,
         'comments' : comments
         }

 # 실제 결과를 출력하는 부분
links =fetch_post_list( )
for link in links :
     result = fetch_post_contents(link)
     print(result)                         
                            
                              
# 위 내용을 파일로 저장하는 부분
def crawler_running():
    links = fetch_post_list()
    with open('post.txt', 'w', encoding='utf-8') as f:
        for link in links:
            result = fetch_post_contents(link)
            f.write('===' * 30 + '\n')
            f.write('글 제목 : ' + result['title'] + '\n')
            f.write('날짜 : ' + result['date'] + '\n')
            f.write('글쓴이 : ' + result['writer'] + '\n')
            f.write('글 내용 : ' + result['content'] + '\n')
            
            if result['comments']:
                f.write('-' * 30)
                f.write('댓글')
                f.write('-' * 30 + '\n')
                count = 1
                for comment in result['comments']:
                    f.write('댓글 ' + str(count) + '\n')
                    f.write('댓글 작성자 : ' + comment['writer'] + '\n')
                    f.write('댓글 등록 날짜 : ' + comment['date'] + '\n')
                    f.write('댓글 내용 : ' + comment['comment_text'] + '\n')
                    count += 1
            f.write('===' * 30 + '\n')
            
            if result['image']:
                image = open( result['title'] + '.jpg', 'wb')
                down_img = urllib.request.urlopen(result['image'])
                image.write(down_img.read())
                image.close()
        f.close()

crawler_running()