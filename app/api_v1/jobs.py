from . import api
from flask import jsonify, request, current_app, g
from flask import send_from_directory
from sqlalchemy import func
from sqlalchemy import or_
import os ,re, time
import hashlib
import json

import importlib

from app.utils import lect_request,atoi
from app import models

from pypinyin import pinyin
import jieba

from app.phrase import deal_acsii,split_article,word2pinyin,add_word

@api.route("/words", methods=['POST'])
def add_words():
        row = lect_request(request, 'word freq grade section know')
        try:
            val=row.pop('word','')
            add_word(val.strip(),row)
            return jsonify(status=200, seqs=val, data=row)
        except Exception as e:
            return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/words/<key>", methods=['PUT'])
def update_words(key):
    try:
        lect = lect_request(request, 'word,freq,grade,section,know,phrase',None)
        row={k:lect[k] for k in lect if lect[k] is not None}
        if row:
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
def delete_words(key):
    try:
        if models.Words.remove(key):
            return jsonify(status=200, message='删除成功')
        else:
            return jsonify(status=404, message='不存在')
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/words/<gbk>", methods=['GET'])
def get_words(gbk):
    try:
        words = models.Words.query.get(gbk)
        if words:
            row = words.to_dict()
            return jsonify(status=200, data=row)
        else:
            return jsonify(status=404, message='不存在')
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/words", methods=['GET'])
def list_words():
    try:
        result=[]
        all = models.Words.query.all()
        for one in all:
            result.append(row.to_dict())
        return jsonify(status=200, data=result)
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/section", methods=['POST'])
def add_section():
    try:
        row = lect_request(request, 'grade chapter know word phrase')
        # for k in row:
        #     row[k]=row[k].decode()

        section=models.Section(**row)
        section.save()
        return jsonify(status=200, data=row)
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/phrase", methods=['POST'])
def add_phrase():
    try:
        param=dict(freq=1,grade=0,section=0,know=0)
        raws=deal_acsii(request.data)
        arr=split_article(raws)
        for wds in arr:
            try:
                phrase = models.Phrase(**wds)
                phrase.save()
            except Exception as e:
                phrase.rollback()
            else:
                word=wds.get('words')
                add_word(word,param)
        return jsonify(status=200, message='成功添加词组数%d'%len(arr))
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))
