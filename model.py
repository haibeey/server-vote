from flask_sqlalchemy import SQLAlchemy
import re
import json

email_matcher=re.compile("[a-z 0-9 A-Z]+@[a-z]+.com")

db=SQLAlchemy()

class User(db.Model):
    __tablename__="users"

    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(30))
    last_name=db.Column(db.String(30))
    email=db.Column(db.String(50))
    password=db.Column(db.String(50))
    image=db.Column(db.String(100),default="today")
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())


    def __repr__(self):
        return str((self.first_name,self.last_name,self.email,self.password,self.image,self.date_created))


class choice(db.Model):
    __tablename__="choices"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30))
    topic=db.Column(db.Integer,db.ForeignKey("topics.id"))
    count=db.Column(db.Integer)
    imagename=db.Column(db.String(70))
    Topic=db.relationship("Topic",backref="choices")

    def __repr__(self):
        return self.name

class Topic(db.Model):
    __tablename__="topics"

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(1000))
    count=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey(User.id))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    users=db.relationship(User,backref="topics")

    def __repr__(self):
        return (self.title)



def match_email(email):
    print(email_matcher.match(email))
    return True if email_matcher.match(email) else False

def string_matcher(string1,string2):
    return string1 in string2


#user=User(first_name="abraham",last_name="abraham",email="email",password="jjsnjss")
#print(user.topics)
#t=Topic(title="vscode vs atom",count=0,users=user)
#y=Topic(title="nigerian vs argentina",count=0,users=user)
#c1=choice(name="vscode",Topic=t)
#c2=choice(name="atom",Topic=t)

#print(user.topics,user)

#db.create_all()
