from app import models
from pypinyin import pinyin
import jieba
import re

def deal_acsii(raws):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    text=raws.decode()
    return re.sub(pattern,'', text)


def word2pinyin(word):
    try:
        g=word.encode('gbk')
        h=g.hex()
        i=int(h, 16)
        tone = '  '.join(pinyin(word,heteronym = True)[0])
        spell = pinyin(word, style =0)[0][0]
        return dict(id=i,gbk=h, word=word, tone=tone, spell=spell)
    except Exception as ee:
        print(str(ee))


def split_article(data):
    phrase=[]
    result = jieba.cut(data)
    for word in result:
        word=word.strip()
        if len(word)>1:
            p=[w[0] for w in pinyin(word)]
            s = ' '.join(p)
            gbk = word.encode('gbk')
            h = gbk.hex()
            phrase.append(dict(gbk=h,score=0,length=len(word),spell=s,words=word))
    return phrase


def add_word(seqs,param):
    for word in seqs:
        try:
            spell = word2pinyin(word)
            spell.update(param)
            words = models.Words(**spell)
            words.save()
        except Exception as ee:
            words.rollback()
            print(str(ee))
