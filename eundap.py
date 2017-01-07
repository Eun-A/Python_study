import urllib.request
from bs4 import BeautifulSoup
import re
import os

list_url = "http://eungdapso.seoul.go.kr/Shr/Shr01/Shr01_lis.jsp"
detail_url = "http://eungdapso.seoul.go.kr/Shr/Shr01/Shr01_vie.jsp"

def get_save_path():
    save_path = str(input("저장할 위치와 파일명을 적어주세요. :" ))
    save_path = save_path.replace("\\", "/")

    if not os.path.isdir(os.path.split(save_path)[0]):
        os.mkdir(os.path.split(save_path)[0])

    return save_path

def fetch_list_url():
    request_header = urllib.parse.urlencode({"page" : "1"})
    request_header = request_header.encode("utf-8")
    url = urllib.request.Request(list_url, request_header)
    res = urllib.request.urlopen(url).read().decode("utf-8")

    bs = BeautifulSoup(res, "html.parser")
    listbox = bs.find_all("li", class_="pclist_list_tit2")
    params = []
    for i in listbox:
        params.append(re.search("[0-9]{14}", i.find("a")["href"]).group())
    
    return params

def fetch_detail_url():
    params = fetch_list_url()

    f = open(get_save_path(), 'w', encoding="utf-8")
    
    for p in params:
        
        request_header = urllib.parse.urlencode({"RCEPT_NO" : str(p)})
        request_header = request_header.encode("utf-8")

        url = urllib.request.Request(detail_url, request_header)
        res = urllib.request.urlopen(url).read().decode("utf-8")
        
        bs = BeautifulSoup(res, "html.parser")
        div = bs.find("div", class_="form_table")
        
        tables = div.find_all("table")

        info = tables[0].find_all("td")

        title = info[0].get_text(strip=True)
        date = info[1].get_text(strip=True)
        
        question = tables[1].find("div", class_="table_inner_desc").get_text(strip=True)
        answer = tables[2].find("div", class_="table_inner_desc").get_text(strip=True)
        

        f.write("==" * 30 + "\n")
        
        f.write(title + "\n")
        f.write(date + "\n")
        f.write(question + "\n")
        f.write(answer + "\n")
        
        f.write("==" * 30 + "\n")

fetch_detail_url()