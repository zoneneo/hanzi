from . import api
from flask import jsonify, request

from app.utils import lect_request,atoi
from app import models


@api.route("/publisher", methods=['POST'])
def add_publisher():
    try:
        row = lect_request(request, 'publishing_house serial_number province')
        publisher=models.Publisher(**row)
        publisher.save()
        return jsonify(status=200, data=publisher.to_dict())
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


@api.route("/book", methods=['POST'])
def add_book():
    try:
        row = lect_request(request, 'title level course grade volume edition editor abstract isbn press province')
        book=models.TextBook(**row)
        book.save()
        return jsonify(status=200, data=book.to_dict())
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))



@api.route("/courses", methods=['POST'])
def add_courses():
    try:
        row = lect_request(request, 'grade chapter know word phrase')
        section=models.Courses(**row)
        section.save()
        return jsonify(status=200, data=row)
    except Exception as e:
        return jsonify(status=500, message='处理错误',error=str(e))


