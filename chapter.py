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

app.app_context().push()


def web_peel(web):
    try:
        match = re.search(r'<div id="vv">', web, re.M|re.I|re.S)
        i,j=match.span()
        body=web[i:]
        match = re.search(r'<p>(.*?)</p>', body, re.M|re.I|re.S)
        i,j=match.span()
        body=body[i:]
        match = re.search(r'</div>', body, re.M|re.I|re.S)
        i,j=match.span()
        return body[:j]

    except Exception as e:
        print(str(e))


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
    try:
        all = models.Links.query.all()
        for o in all:
            dat = get_web(o.link)
            web = web_peel(dat)
            try:
                chapter=models.Chapter(content=web,grade=o.grade,chapter=o.chapter,subject=o.subject)
                chapter.save()
            except Exception as e:
                chapter.rollback()
    except Exception as e:
        print(str(e))



if __name__ == '__main__':
    deal_grab()


