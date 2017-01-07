import facebook
obj = facebook.GraphAPI(access_token="EAACEdEose0cBAIIvxZA2hdhfthmVZBCZC6YTQLv93HJw3vmrCZCWrZB7PlDwRforTEi43sJbv9kzap4xJfGs1iUrlSNpHEGjEHUStnjUVzGDX4DQwJZAZCXX3kcSd0Spuyvgl6Qxbr2zpYIlFsZAXF7qr9PpJmazipUtYGasXDexJwZDZD")
limit = int(raw_input("몇건의 게시물을 검색할까요? "))
response = obj.get_connections(id="me", connection_name="posts", limit=limit)
f = open("C:/Users/Eun_A/Desktop", "w")

for data in response[u"data"]:
f.write("==" * 30 + "\n")
f.write("게시물 작성자 : " + data[u"from"][u"name"].encode("utf-8") + "\n")
f.write("게시물 아이디 : " + data[u"from"][u"id"].encode("utf-8") + "\n")
f.write("최종 업데이트 시간 : " + data[u"updated_time"].encode("utf-8") + "\n")
f.write("게시물 링크 : " + data[u"actions"][0][u"link"].encode("utf-8") + "\n")
if u"message" in data:
	f.write("게시물 내용 : " + data[u"message"].encode("utf-8") + "\n")
if u"picture" in data:
	f.write("게시물 사진 이름 : " + data[u"name"].encode("utf-8") + "\n")
	f.write("사진 주소 : " + data[u"picture"].encode("utf-8") + "\n")
if u"description" in data:
	f.write("사진 설명 : " + data[u"description"].encode("utf-8") + "\n")
f.write("==" * 30 + "\n")
f.close()