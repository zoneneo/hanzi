from urllib import parse
from urllib import request
import requests
import os
import re

link=parse.urlparse('https://www.thn21.com/xiao/special/kewen/xxkw1.html')


# d = {'client_id':7,'type':'tcp','remark':'','port':8007,'target':22,'auth_key': crypt, 'timestamp': tms}
# r = requests.post(url, data=d)

body_pt= re.compile(r'<table[^>]*>.*</table>')
#subject_pt = re.compile(r'<td>(\d+)[^<]*<a\s+href="([^"]*)"[^>]*>([^<]*)</a>')
subject_pt = re.compile(r'<td>(\d+)[^<]*<a\s+href="([^"]*)"[^>]*>([^<]*)</a>')
subject_pt2 = re.compile(r'<a\s+href="([^"]*)"[^>]*>(\d+)([^<]*)</a>')
urls=[]
path=os.path.dirname(link.path)

for i in range(1,13):
    basename='xxkw%d.html'%i
    uri=os.path.join(path, basename)
    url=link._replace(path=uri).geturl()
    urls.append(url)


def readfile(file):
    chunk_size = 512
    txt = ''
    with open(file,'r') as fp:
        while True:
            c=fp.read(chunk_size)
            if c=='':
                break
            else:
                txt +=c
    return txt



def web_peel(web):
    try:
        match=re.search(r'<table[^>]*>.*</table>',web,re.M|re.I|re.S)
        if not match:
            match = re.search(r'(<p>(.*)</p>)+', web, re.M|re.I|re.S)
            text = match.group()
            #text=re.sub(r'<(\/)?(p)>',r'<\1td>',text,re.M|re.I|re.S)
        else:
            text=match.group()
    except:
        text =content
    return text

def cleaning(content):
    content = content.replace('&nbsp;',' ')
    content=re.sub(r'<\/?font([^>]*)?>','', content, re.M|re.I)
    return content

def deal_content(body):
    #it = re.findall(r'("\d+\.")?[^<]*<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', body, re.M |re.I|re.S)
    it = re.findall(r'<td>(\d+\.)?<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', body, re.M | re.I | re.S)
    if not it:
        it = re.findall(r'<p>(\d+\.)?<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', body, re.M | re.I | re.S)
    print(it)

def get_web(url):
    try:
        req=requests.get(url)
        if req.content !='':
            encoding=req.apparent_encoding
            return req.content.decode(encoding)
        else:
            return ''
    except Exception as e:
        print(str(e))

urls=['https://www.thn21.com/xiao/special/kewen/xxkw7.html','https://www.thn21.com/xiao/special/kewen/xxkw9.html']
for url in urls:
    print(url)
    web=get_web(url)
    content=web_peel(web)
    body=cleaning(content)
    deal_content(body)


# try:
#     content = readfile('kwmb9.txt')
#     deal_content(cleaning(content))
# except Exception as e:
#     print(str(e))
