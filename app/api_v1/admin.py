from . import api
from flask import jsonify, request

from app.utils import lect_request,atoi
from app import models


# from app.phrase import deal_acsii,split_article,word2pinyin,add_word
#
# @api.route("/words", methods=['POST'])
# def add_words():
#         row = lect_request(request, 'word freq grade section know')
#         try:
#             val=row.pop('word','')
#             add_word(val.strip(),row)
#             return jsonify(status=200, seqs=val, data=row)
#         except Exception as e:
#             return jsonify(status=500, message='处理错误',error=str(e))
#
#
# @api.route("/words/<key>", methods=['PUT'])
# def update_words(key):
#     try:
#         lect = lect_request(request, 'word freq grade section know phrase',None)
#         row={k:lect[k] for k in lect if lect[k] is not None}
#         w=row.pop('word')
#         if row:
#             pin=word2pinyin(w)
#             row.update(pin)
#             word = models.Words(**row)
#             word.upsert()
#             return jsonify(status=200, data=row)
#         else:
#             return jsonify(status=400, message='没有修改内容')
#     except Exception as e:
#         return jsonify(status=500, message='处理错误',error=str(e))
#
#
# @api.route("/words/<key>", methods=['DELETE'])
# def delete_words(key):
#     try:
#         if models.Words.remove(key):
#             return jsonify(status=200, message='删除成功')
#         else:
#             return jsonify(status=404, message='不存在')
#     except Exception as e:
#         return jsonify(status=500, message='处理错误',error=str(e))
#
#
# @api.route("/words/<gbk>", methods=['GET'])
# def get_words(gbk):
#     try:
#         words = models.Words.query.get(gbk)
#         if words:
#             row = words.to_dict()
#             return jsonify(status=200, data=row)
#         else:
#             return jsonify(status=404, message='不存在')
#     except Exception as e:
#         return jsonify(status=500, message='处理错误',error=str(e))
#
#
# @api.route("/words", methods=['GET'])
# def list_words():
#     try:
#         z,n,f,v=lect_request(request, 'size','page','field','value')
#         pgz,pgn=atoi(z,2),atoi(n,1)
#         if f and v:
#             parms={f:v}
#         else:
#             parms={}
#         result=[]
#         query = models.Words._page(pgn,pgz,**parms)
#
#         for one in query.items:
#             result.append(one.to_dict())
#         return jsonify(status=200, data=result)
#     except Exception as e:
#         return jsonify(status=500, message='处理错误',error=str(e))
#
#
# @api.route("/section", methods=['POST'])
# def add_section():
#     try:
#         row = lect_request(request, 'grade chapter know word phrase')
#         section=models.Section(**row)
#         section.save()
#         return jsonify(status=200, data=row)
#     except Exception as e:
#         return jsonify(status=500, message='处理错误',error=str(e))
#
#
# @api.route("/phrase", methods=['POST'])
# def add_phrase():
#     try:
#         param=dict(freq=1,grade=0,section=0,know=0)
#         raws=deal_acsii(request.data)
#         arr=split_article(raws)
#         for wds in arr:
#             try:
#                 phrase = models.Phrase(**wds)
#                 phrase.save()
#             except Exception as e:
#                 phrase.rollback()
#             else:
#                 word=wds.get('words')
#                 add_word(word,param)
#         return jsonify(status=200, message='成功添加词组数%d'%len(arr))
#     except Exception as e:
#         return jsonify(status=500, message='处理错误',error=str(e))
#
#
#
# @api.route("/phrase", methods=['GET'])
# def list_phrase():
#     try:
#         z,n,f,v=lect_request(request, 'size','page','field','value')
#         pgz,pgn=atoi(z,2),atoi(n,1)
#         if f and v:
#             parms={f:v}
#         else:
#             parms={}
#         result=[]
#         query = models.Phrase._page(pgn,pgz,**parms)
#
#         for one in query.items:
#             result.append(one.to_dict())
#         return jsonify(status=200, data=result)
#     except Exception as e:
#         return jsonify(status=500, message='处理错误',error=str(e))



