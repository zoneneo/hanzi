# -*- coding: utf-8 -
from .exts import db
from sqlalchemy import Column, text, func, Index, outerjoin, and_
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import distinct
from sqlalchemy import desc
from sqlalchemy import update
from sqlalchemy.orm import aliased

from sqlalchemy.types import TypeDecorator, VARCHAR
import sqlalchemy.types as types
from sqlalchemy.ext.mutable import Mutable,MutableDict,MutableList
import json

lett=db.Enum()
a=ord('a')
lett.enums=[chr(i) for i in range(a,a+26)]


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string."""

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


#MutableDict.associate_with(JSONEncodedDict)


class Base(db.Model):
    __abstract__ = True
    __table_args__ = {'mysql_engine': 'InnoDB'}
    # create_time = db.Column(db.TIMESTAMP(True),server_default=text('CURRENT_TIMESTAMP'))
    @declared_attr
    def __tablename__(cls):
        return 'c'+''.join([c.isupper() and '_'+c or c for c in cls.__name__]).lower()

    def save(self, flush = True):
        result = db.session.add(self)
        if flush:
            #db.session.flush()
            db.session.commit()
        return result

    def destroy(self):
        result = db.session.delete(self)
        return result

    def to_dict(self):
        d = dict()
        for c in self.__table__.columns:
            v = getattr(self, c.name)
            if v:
                d[c.name] = v
        return d


    @classmethod
    def update(cls,sid,**row):
        cls.query.filter_by(id=sid).update(row)
        return db.session.commit()


    @classmethod
    def by_id(cls, id):
        return cls.query.get(id)


    @classmethod
    def remove(cls, kid):
        one = cls.query.get(kid)
        db.session.delete(one)
        return db.session.commit()


    @classmethod
    def delete(cls, ids):
        result = (cls.query
            .filter(cls.id.in_(ids))
            .delete(synchronize_session=False))
        return result


    @classmethod
    def get_count(cls, search = None):
        result = db.session.query(func.count(cls.id))
        return result.scalar()

    @classmethod
    def commit(cls):
        db.session.commit()


class Common(Base):
    key = db.Column(db.String(128), primary_key=True)
    value = db.Column(db.String(1024))

class User(Base):
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    username = db.Column(db.String(100),comment= '姓名')
    password = db.Column(db.String(128),comment= '密码')
    email = db.Column(db.String(128),comment= '邮箱')
    role = db.Column(db.String(6),comment= '角色')


class Customer(Base):
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    name = db.Column(db.String(100),comment= '姓名')
    age = db.Column(db.String(100),comment= '年龄')
    sex = db.Column(db.String(100),comment= '性别')
    birthday = db.Column(db.Integer,comment= '出生日期')
    nation = db.Column(db.String(100),comment= '民族')
    phone = db.Column(db.String(16),comment= '联系电话')
    email = db.Column(db.String(128),comment= '邮箱')
    address = db.Column(db.String(64),comment= '联系地址')
    idcard = db.Column(db.String(20),comment= '身份证号码')
    native_place = db.Column(db.String(64),comment= '籍贯')
    remark = db.Column(db.String(128),comment= '备注')


class Study(Base):
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)

class Students(Base):
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)


#汉语字词
class Words(Base):
    id = db.Column(db.Integer, primary_key=True)
    spell = db.Column(db.String(16), comment='拼音')
    letter = db.Column(lett, comment='首字母')
    word = db.Column(db.String(8), comment='汉字')
    freq = db.Column(db.Integer, comment='频率')
    grade = db.Column(db.Integer, comment='年级')
    section = db.Column(db.String(64), comment='章节')
    know = db.Column(db.Integer, comment='牚握')
    phrase = db.Column(db.String(512), comment='词组')


#四字成语
class Idiom(Base):
    id = db.Column(db.Integer, primary_key=True)


#词组短语
class Phrase(Base):
    id = db.Column(db.Integer, primary_key=True)
    audit = db.Column(db.Boolean(0), comment='是否正确')
    kind = db.Column(db.Enum('a','i','p','w'), comment='分类idiom,proverb,word')
    spell = db.Column(db.String(128), comment='拼音')
    words = db.Column(db.String(32), comment='词组')


