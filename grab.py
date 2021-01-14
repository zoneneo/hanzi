from urllib import parse
from urllib import request
import requests
import os
import re

from app import create_app
from app.exts import db
app = create_app()
db.init_app(app)

from app import models

#app.run(host='0.0.0.0', debug=True)
app.app_context().push()
link=parse.urlparse('https://www.thn21.com/xiao/special/kewen/xxkw1.html')


# d = {'client_id':7,'type':'tcp','remark':'','port':8007,'target':22,'auth_key': crypt, 'timestamp': tms}
# r = requests.post(url, data=d)

urls=[]
path=os.path.dirname(link.path)


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
        text =web
    return text


def deal_content(body):
    #it = re.findall(r'(<td>|<p>)(\d+\.)?<a\s+href="([^"]*)"[^>]*>([^<]*)</a>', body, re.M | re.I | re.S)
    #上面不能包含如后格式</a href=""><font>xxx</font></a>
    all=[]
    dat = re.findall(r'(?:<td>|<p>)(\d+)?[\.\s]?<a\s+href="([^"]*)"[^>]*>(.*?)</a>', body, re.M | re.I | re.S)
    for it in dat:
        i,t,s=it
        s=s.replace('&nbsp;',' ').replace('\u3000','')
        s=re.sub(r'</?\w+[^>]*>', '', s, re.M | re.I)
        tag=s.split(' ')[0]
        tag=tag.replace('课文原文','')

        if i=='':
            m = re.search(r'^\d+', tag)
            i=m.group()
        l = link._replace(path=t).geturl()
        all.append((i,l,tag))
    return all

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

def deal_grab():
    for n in range(1,13):
        try:
            basename='xxkw%d.html'%n
            uri=os.path.join(path, basename)
            url=link._replace(path=uri).geturl()
            print(url)
            web=get_web(url)
            body=web_peel(web)
            arr=deal_content(body)
            for a in arr:
                j,l,s=a
                links = models.Links(grade=n,chapter=j,link=l,subject=s)
                links.save()
        except Exception as e:
            print(str(e))


deal_grab()
