import json
from . import api
from flask import jsonify, request, current_app, g
from app.utils import lect_request,atoi,object_dict
from app.models import Common


@api.route("/common/<key>", methods=['POST'])
def add_common(key):
    try:
        value = lect_request(request)
        if key and value:
            Common(key=key,value=json.dumps(value)).save()
            return jsonify(status=200, key=key, value=value)
        else:
            return jsonify(status=400, message='不能为空')
    except Exception as e:
        return jsonify(status=500, message='处理错误', error=str(e))


@api.route("/common/<key>", methods=['PUT'])
def add_comm_any(key):
    all = lect_request(request)
    if all:
        com=Common.query.filter(Common.key == key).first()
        try:
            val = json.loads(com.value)
            val.append(all)
            Common.query.filter(Common.key == key).update({'value':json.dumps(val)})
            Common.commit()
        except:
            value=json.dumps([all])
            Common(key=key,value=value).save()
        return jsonify(status=200, data=all)
    else:
        return jsonify(status=400, message='不能为空')


@api.route("/common/<key>", methods=['DELETE'])
def del_comm_key(key):
    try:
        com = Common.query.filter(Common.key == key).first()
        row=com.to_dict()
        com.destroy()
        Common.commit()
        return jsonify(status=200, data=row)
    except Exception as e:
        return jsonify(status=404, message=str(e))


@api.route("/common/<key>/<inx>", methods=['PUT'])
def put_comm_any(key,inx):
    if not inx.isdigit():
        return jsonify(status=400, message='编号必需是数字')
    i=int(inx)-1
    if i < 0:
        return jsonify(status=400, message='编号必需大于等于1')
    all = lect_request(request)
    if all:
        row = Common.query.filter(Common.key == key).first()
        try:
            val = json.loads(row.value)
            old=val.pop(i)
            val.insert(i,all)
            ret = Common.query.filter(Common.key == key).update({'value':json.dumps(val)})
            Common.commit()
            return jsonify(status=200, old=old, data=all )
        except Exception as e:
            return jsonify(status=404, message='项目不存在')

    else:
        return jsonify(status=400, message='不能为空')


@api.route("/common/<key>/<inx>", methods=['DELETE'])
def del_comm_any(key,inx):
    if not inx.isdigit():
        return jsonify(status=400, message='编号必需是数字')
    com = Common.query.filter(Common.key == key).first()
    try:
        val = json.loads(com.value)
        one = val.pop(int(inx) - 1)
        ret = Common.query.filter(Common.key == key).update({'value':json.dumps(val)})
        Common.commit()
        one['id']=inx
        return jsonify(status=200, data=one)
    except Exception as e:
        return jsonify(status=404, message='项目不存在')


@api.route("/common/<key>/<inx>", methods=['GET'])
def get_comm_any(key,inx):
    if not inx.isdigit():
        return jsonify(status=400, message='编号必需是数字')
    com = Common.query.filter(Common.key == key).first()
    try:
        val = json.loads(com.value)
        one = val.pop(int(inx) - 1)
        one['id']=inx
        return jsonify(status=200, data=one)
    except Exception as e:
        return jsonify(status=404, message='项目不存在')


@api.route("/common/<key>", methods=['GET'])
def get_comm_key(key):
    com = Common.query.filter(Common.key == key).first()
    try:
        data=json.loads(com.value)
        for i in range(len(data)):
            data[i]['id']=i+1
        return jsonify(status=200, data=data)
    except Exception as e:
        return jsonify(status=404, message='对象不存在',error=str(e))


@api.route("/common", methods=['GET'])
def get_common_all():
    try:
        result = []
        for one in Common.query.all():
            row = object_dict(one)
            try:
                row['value'] = json.loads(row['value'])
            except:
                pass
            result.append(row)
        return jsonify(status=200, data=result)
    except Exception as e:
        return jsonify(status=500, message='处理错误', error=str(e))


