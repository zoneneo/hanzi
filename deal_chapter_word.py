import os
import re

from app.phrase import word2pinyin

from app import create_app
from app.exts import db
from app import models

app = create_app()
db.init_app(app)
app.app_context().push()

res=set()
#字符按编码去重
pattern = re.compile(r'[^\u4e00-\u9fa5]')
all=models.Chapter._all()
for row in all:
    try:
        txt = re.sub(pattern, '', row.content)
    except Exception as e:
        print(e)
    else:
        tmp=set(txt)
        res = res.union(tmp)

for a in res:
    try:
        row=word2pinyin(a)
        words = models.Words(**row)
        words.save()
    except Exception as ex:
        print('at',a)
        print(str(ex))