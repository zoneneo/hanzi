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

# lett=db.Enum()
# a=ord('a')
# lett.enums=[chr(i) for i in range(a,a+26)]


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

def tab_name(val,pre='c'):
    seq=pre+val
    return ''.join([c.isupper() and '_'+c or c for c in seq]).lower()



class Base(db.Model):
    __abstract__ = True
    __table_args__ = {'mysql_engine': 'InnoDB'}
    # create_time = db.Column(db.TIMESTAMP(True),server_default=text('CURRENT_TIMESTAMP'))

    @declared_attr
    def __tablename__(cls):
        return tab_name(cls.__name__)

    def save(self, flush = True):
        result = db.session.add(self)
        if flush:
            #db.session.flush()
            db.session.commit()
        return result

    def upsert(self):
        db.session.merge(self)
        return db.session.commit()

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
    def rollback(cls):
        return db.session.rollback()


    @classmethod
    def update(cls,sid,**row):
        cls.query.filter_by(id=sid).update(row)
        return db.session.commit()


    @classmethod
    def _get(cls, key):
        return cls.query.get(key)


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
    def _count(cls, search = None):
        result = db.session.query(func.count(cls.id))
        return result.scalar()

    @classmethod
    def commit(cls):
        db.session.commit()

    @classmethod
    def _search(cls, page, size, **search):

        is_desc = search.pop('is_desc',False)
        if search:
            key, val = search.popitem()
            if key in cls.__table__.columns:
                field = getattr(cls, key)
                query = cls.query.filter(field.like("%" + val + "%"))
            else:
                query = cls.query
        else:
            query = cls.query

        if is_desc:
            query = query.order_by(desc(cls.id))
        else:
            query = query.order_by(cls.id)

        return query.paginate(page, per_page=size, error_out=False)

    @classmethod
    def _page(cls, page, size, **kwargs):
        is_desc = kwargs.pop('is_desc',False)
        if kwargs:
            conditions={}
            for key in kwargs:
                if key in cls.__table__.columns:
                    conditions[key]=kwargs[key]
            query = cls.query.filter_by(**conditions)
        else:
            query = cls.query

        if is_desc:
            query = query.order_by(desc(cls.id))
        else:
            query = query.order_by(cls.id)

        return query.paginate(page, per_page=size, error_out=False)

    @classmethod
    def _all(cls):
        return cls.query.all()


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
    gbk = db.Column(db.String(8), comment='编码')
    spell = db.Column(db.String(50), comment='拼写')
    word = db.Column(db.String(4), comment='汉字')
    tone = db.Column(db.String(50), comment='拼音')
    freq = db.Column(db.Integer, comment='频率')

#四字成语
class Idiom(Base):
    id = db.Column(db.Integer, primary_key=True)

#格言谚语
class Proverb(Base):
    id = db.Column(db.Integer, primary_key=True)

#词组短语
class Phrase(Base):
    id = db.Column(db.Integer, primary_key=True)
    gbk=db.Column(db.String(16),unique=True, comment='编码')
    score = db.Column(db.Boolean(0), comment='评分')
    length = db.Column(db.Integer, comment='词组长度')
    spell = db.Column(db.String(128), comment='拼音')
    words = db.Column(db.String(32), comment='词组')


class Chapter(Base):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer, comment='年级')
    chapter = db.Column(db.Integer, comment='章节')
    subject = db.Column(db.String(64), comment='题目')
    content = db.Column(db.Text, comment='课文')


class Section(Base):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer, comment='年级')
    chapter = db.Column(db.Integer, comment='章节')
    know = db.Column(db.String(512), comment='识字表')
    word = db.Column(db.String(512), comment='写字表')
    phrase = db.Column(db.Text, comment='词语表')


class Dictation(Base):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, comment='课本id')
    grade = db.Column(db.Integer, comment='年级')
    chapter = db.Column(db.String(64), comment='章节')
    words = db.Column(db.String(64), comment='写字表')
    know = db.Column(db.String(64), comment='识字表')
    phrase = db.Column(db.String(512), comment='词组')


class Courses(Base):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, comment='课本id')
    grade = db.Column(db.Integer, comment='年级')
    chapter = db.Column(db.String(64), comment='章节')
    words = db.Column(db.String(64), comment='写字表')
    know = db.Column(db.String(64), comment='识字表')
    phrase = db.Column(db.String(512), comment='词组')


class Article(Base):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), comment='标签')
    book_id = db.Column(db.Integer, comment='书本id')
    category = db.Column(db.String(64), comment='分类')
    author = db.Column(db.String(32), comment='作者')
    subject = db.Column(db.String(64), comment='主题')
    content = db.Column(db.Text, comment='内容')


class TextBook(Base):
    id = db.Column(db.Integer, primary_key=True)
    #publication_date = db.Column(db.TIMESTAMP(True), server_default=text('CURRENT_TIMESTAMP'))
    title =db.Column(db.String(64), comment='书本名称')
    course = db.Column(db.String(32), comment='科目')#语文
    level = db.Column(db.String(64), comment='级别')#小初中高级
    grade = db.Column(db.Integer, comment='年级')
    volume = db.Column(db.Integer, comment='上中下册')
    edition=db.Column(db.String(64), comment='版本')
    editor=db.Column(db.String(128), comment='主编')
    abstract=db.Column(db.Text, comment='摘要')
    isbn = db.Column(db.String(32), comment='版本')
    press=db.Column(db.Integer, comment='出版商id')
    province = db.Column(db.Integer, comment='省份')


class Publisher(Base):
    id = db.Column(db.Integer, primary_key=True)
    publishing_house = db.Column(db.String(128), comment='出版商')
    serial_number = db.Column(db.String(8), comment='编号')
    province = db.Column(db.Integer, comment='省份')



class Links(Base):
    id = db.Column(db.Integer, primary_key=True)
    used = db.Column(db.Boolean(0), comment='己使用')
    grade = db.Column(db.Integer, comment='年级')
    chapter = db.Column(db.Integer, comment='课文')
    subject = db.Column(db.String(64), comment='课文题目')
    link = db.Column(db.String(512), comment='链接')
    tag = db.Column(db.String(16), comment='标签')