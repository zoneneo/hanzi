from . import api
from flask import jsonify, request, current_app, g
from flask import send_from_directory
from sqlalchemy import func
from sqlalchemy import or_
import os ,re, time
import hashlib
import json

import importlib

from app.utils import lect_request,atoi,str_to_list,object_dict
from app import models

from pypinyin import pinyin
import jieba

from io import BytesIO

@api.route("/words", methods=['POST'])
def add_words():
    try:
        #row = lect_request(request,' id spell word freq grade section know phrase')
        row = lect_request(request, 'word freq grade section know')
        wds=row.get('word','').split()
        if len(wds)>1:
            for w in wds:
                row['word']=w
                row['spell']=pinyin(w)[0][0]
                customer = models.Words(**row)
                customer.save()
        else:
            row['spell'] = pinyin(row['word'])[0][0]
            customer = models.Words(**row)
            customer.save()
        return jsonify(status=200, data=row)
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/words/<key>", methods=['PUT'])
def update_customer(key):
    try:
        lect = lect_request(request, 'word,freq,grade,section,know,phrase',None)
        row={k:lect[k] for k in lect if lect[k] is not None}
        if row:
            #ret = models.Words.query.filter(models.Words.id == key).update(row)
            #current_app.session.commit()
            ret = models.Words.update(key,**row)
            if ret:
                row['id']=key
                return jsonify(status=200, data=row)
            else:
                return jsonify(status=404, message='项目不存在')
        else:
            return jsonify(status=400, message='没有修改内容')
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/words/<key>", methods=['DELETE'])
def delete_customer(key):
    try:
        if models.Words.remove(key)：
            return jsonify(status=200, message='删除成功')
        else:
            return jsonify(status=404, message='不存在')
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/words/<uid>", methods=['GET'])
def get_customer(uid):
    try:
        customer = models.Words.query.get(uid)
        if customer:
            row = object_dict(customer)
            return jsonify(status=200, data=row)
        else:
            return jsonify(status=404, message='客户不存在')
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/words", methods=['GET'])
def get_customers():
    try:
        result=[]
        all = models.Words.query.all()
        for one in all:
            row=object_dict(one)
            result.append(row)
        return jsonify(status=200, data=result)
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))



def to_add_word(word):
    try:
        g=word.encode('gbk')
        i=int(g.hex(), 16)
        spell = pinyin(word)[0][0]
        words = models.Words(id=i,word=word, spell=spell, phrase='', know='0', section='', grade='0', freq='0')
        current_app.session.add(words)
        current_app.session.flush()
        current_app.session.commit()
    except Exception as ee:
        current_app.session.rollback()
        print(str(ee))



@api.route("/phrase", methods=['POST'])
def add_phrase():
    try:
        raws=request.data
        pattern = re.compile(r'[^\u4e00-\u9fa5]')
        text=raws.decode()
        data = re.sub(pattern,'', text)
        result = jieba.cut(data)

        arr=[]
        for word in result:
            word=word.strip()
            arr.append(word)
            l=len(word)
            if l>1:
                p=[w[0] for w in pinyin(word)]
                s = ' '.join(p)
                try:
                    gbk = word.encode('gbk')
                    h = gbk.hex()
                    phrase = models.Phrase(gbk=h,score=0,length=l,spell=s,words=word)
                    current_app.session.add(phrase)
                    current_app.session.flush()
                    current_app.session.commit()
                except Exception as ex:
                    current_app.session.rollback()
                    print(str(ex))


        for wds in arr:
            for w in wds:
                to_add_word(w)

        return jsonify(status=200, message='成功添加词组数%d'%len(arr))
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/grab", methods=['get'])
def run_grab():
    from app import grab
    lks=grab.deal_grab()
