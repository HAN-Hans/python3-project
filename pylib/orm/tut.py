import pymysql
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr

def fn():
    return pymysql.Connect(
        host='127.0.0.1',
        user='ubuntu',
        password='spsp1505',
        database='hit'
    )

engine = create_engine(
    # 'sqlite:///:memory:',
    echo=True,
    connect_args=[('charset', 'utf8')],
    creator=fn,
)


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}

    id =  Column(Integer, primary_key=True)
    def __repr__(self):
       return f"{self.id}"


Base = declarative_base(cls=Base)


class User(Base):
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
       return "<User(name='%s', fullname='%s', password='%s')>" % (
           self.name, self.fullname, self.password)


class MyMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__= {'always_refresh': True}

    id =  Column(Integer, primary_key=True)

    @declared_attr
    def address_id(cls):
        return Column(Integer, ForeignKey('address.id'))


class MyModel(MyMixin, Base):
    name = Column(String(1000))


pass