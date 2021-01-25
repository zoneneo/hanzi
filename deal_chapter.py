import os
import re

from app.phrase import word2pinyin,split_article

from app import create_app
from app.exts import db
from app import models

app = create_app()
db.init_app(app)
app.app_context().push()

pattern = re.compile(r'[^\u4e00-\u9fa5]')
all=models.Chapter._all()
for row in all:
    if not row.content:
        continue
    txt = re.sub(pattern, '', row.content)
    arr=split_article(txt)
    for wds in arr:
        try:
            phrase = models.Phrase(**wds)
            #phrase.save()
            phrase.upsert()
        except Exception as e:
            phrase.rollback()