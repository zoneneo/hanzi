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
from app  import models


@api.route("/words", methods=['POST'])
def add_words():
    try:
        row = lect_request(request,'')
        customer = models.Words(**row)
        current_app.session.add(customer)
        current_app.session.commit()

        return jsonify(status=200, data=row)
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/examiner/<uid>", methods=['PUT'])
def update_customer(uid):
    try:
        lect = lect_request(request, 'code name sex age birthday nation phone idcard email address family_desc clinical_desc clinical_data remark treatment family_sick',None)
        row={k:lect[k] for k in lect if lect[k] is not None}
        if row:
            ret = Examiner.query.filter(Examiner.id == uid).update(row)
            current_app.session.commit()
            if ret:
                row['id']=uid
                return jsonify(status=200, data=row)
            else:
                return jsonify(status=404, message='项目不存在')
        else:
            return jsonify(status=400, message='没有修改内容')
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/examiner/<uid>", methods=['DELETE'])
def delete_customer(uid):
    try:
        one = Examiner.query.get(uid)
        if one:
            current_app.session.delete(one)
            current_app.session.commit()
            return jsonify(status=200, message='删除成功')
        else:
            return jsonify(status=404, message='不存在')
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/examiner/<uid>", methods=['GET'])
def get_customer(uid):
    try:
        customer = Examiner.query.get(uid)
        if customer:
            row = object_dict(customer)
            return jsonify(status=200, data=row)
        else:
            return jsonify(status=404, message='客户不存在')
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/examiner", methods=['GET'])
def get_customers():
    try:
        result=[]
        all = Examiner.query.all()
        for one in all:
            row=object_dict(one)
            result.append(row)
        return jsonify(status=200, data=result)
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))



