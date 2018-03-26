import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import re
import json
'''url="http://maoyan.com/board/4?offset=10"
一点都不友好的猫眼，本来打算爬取猫眼T100呢，封我IP
so 转战豆瓣
'''


def get_one_page(url):
    try:
        req = requests.get(url)
        if req.status_code ==200:
            return req.text
        return req.status_code
    except RequestException:
        return None

def parse_one_page(html):
    #pattern=re.compile('<li>.*?<em.*?>(\d*)</em>.*?<img.*?src="(.*?)".*?<span class="title">(.*?)</span>.*?star.*?average">(.*?)</span>.*?inq">(.*?)</span>.*?</li>',re.S)
    pattern = re.compile('<li>.*?<em.*?>(\d*)</em>.*?<img.*?src="(.*?)".*?<span class="title">(.*?)</span>.*?class="bd.*?<p .*?>(.*?)&nbsp.*?:(.*?)<br>(\d*).*?star.*?average">(.*?)</span>.*?inq">(.*?)</span>.*?</li>', re.S)
    items=re.findall(pattern,html)

    for item in items:
        yield{
            "index":item[0],
            "image":item[1],
            "title":item[2],
            "director":item[3].strip()[3:],
            "actor":item[4],
            "grade":item[5],
            "class_sayings":item[6],
        }
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) +'\n')
        f.close()
#json.dumps把字典类型content转换成字符串类型

def main(start):
    url = 'https://movie.douban.com/top250?start='+ str(start)+ '&filter='
    html=get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__=='__main__':
    for i in range(10):
        main(i*10)




