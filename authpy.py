
import json
import os
import sqlalchemy.exc as E
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,ForeignKey,\
            create_engine
from sqlalchemy.orm import relationship,sessionmaker


class base(declarative_base()):
    __tablename__="base"
    Name=Column(Integer,primary_key=True)


class Operation(object):
    def __init__(self):
        engine=create_engine("sqlite:///"+"authj")
        Session=sessionmaker()
        Session.configure(bind=engine)
        self.Session=Session()
        base.metadata.create_all(engine)
    def In(self,name):
        data=None
        try:
            data=self.Session.query(base).filter(base.Name==Hash(name)).first()
        except E.OperationalError:
            print("table not yet created")
            Base=base(Name=Hash(name))
            self.Session.add(Base)
            self.Session.commit()
            return False
        if data:
            return False
        return True
    def insert(self,name):
        if not self.In(name):
            return False
        else:
            Base=base(Name=Hash(name))
            self.Session.add(Base)
            self.Session.commit()
            return True


def Hash(value):
    "you can specify your own hash functions as design hash function is a tricky business"
    d={'a':22,'b':25,'c':7,'d':9,'e':18,'f':21,'g':3,'h':5,'i':6,'j':20,'k':11,'l':13,'m':17,\
           'n':4,'o':2,'p':26,'q':16,'r':1,'s':10,'t':14,'u':19,'v':15,'w':23,'x':12,'y':8,'z':24}
    value=sum([d[i]*ord(i) for i in value if i in d])
    return value%1001

class auth(object):
    def __init__(self):
        self.operation=Operation()

    def insert(self,name):
        return self.operation.insert(name)

    def In(self,name):
        return self.operation.In(name)

#a=auth()
#print(a.insert('request.form["email"]'),Hash('request.form["email"]'))
#print(a.insert('ab'),Hash('ab'))
#print(a.insert('ab'))
#print(a.insert('s'),Hash("s"))
