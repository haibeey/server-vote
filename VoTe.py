from flask import Flask,jsonify,request,session
from werkzeug.security import generate_password_hash, check_password_hash
from authpy import auth
from model import User,Topic,choice,db,match_email,string_matcher
from data import Cache,Ip
from flask import g,render_template,url_for,redirect,flash,send_file,send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename


vote =Flask(__name__)
Auth=auth()
cache=Cache()
ip=Ip()

vote.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///VOOTE'
#vote.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
vote.config["SECRET_KEY"]="6g73vut6svs766rdfd"
vote.config['DATABASE']='myblog.db'
vote.config["UPLOAD_FOLDER"]="/home/haibeeyy/mysite/uploads"
Allowed_extensions=set(["png","jpeg"])



db.init_app(vote)
db.create_all(app=vote)

per_query=30
def onError(error=None):
    "returns some json object with error"
    if error:
        j_data={
            "response":"error",
            "message":str(error)
        }
    else:
        j_data={
        "response":"error",
        "message":"invalid parameters"
    }
    return jsonify(j_data)

def json_message(response,message):
    return {
            "response":response,
            "message":message
        }


@vote.route("/",methods=["GET"])
def home():
    result={} #would hold the result for all data that would be sent back to the client
    arg=request.args.get("name")
    if arg:
        user_topic=User.query.filter_by(email=arg).first().topics
        t_opics=[]
        incremental=1
        for t_ in user_topic:
            arr=[t_.title,t_.count]
            to_be_added={
                "topic":arr
            }
            t_opics.append(to_be_added)
            incremental=incremental+1
        result["users"]=t_opics
    else:
        result["users"]=[]

    category=int(request.args.get("category"))
    all_topic=Topic.query.all()
    all_topic.reverse()
    t_opics=[]
    for topic in all_topic[category*per_query-per_query:category*per_query]:
        Dict={
            "title":topic.title,
            "choices":[[choice.name,choice.count] for choice in topic.choices],
            "created_by":topic.users.first_name,
            "date":topic.date_created,
            "count":topic.count
        }
        t_opics.append(Dict)
    result["topics"]=t_opics
    result["response"]="ok"
    return jsonify(result)
@vote.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="GET":
        return jsonify(json_message("error","unsupported request method"))
    first_name=request.form["firstname"]
    last_name=request.form["lastname"]
    email=request.form["email"]
    password=request.form["password"]
    if Auth.In(email):
        if match_email(email):
            if "file" not in request.files:
                return jsonify(json_message("error","invalid filename"))
            file=request.files["file"]
            if not file.filename:
                return  jsonify(json_message("error","invalid filename"))
            if not file or file.filename.split(".")[-1] in Allowed_extensions:
               return jsonify(json_message("error","invalid file type"))
            secure_name=secure_filename(file.filename)
            file.save(os.path.join(vote.config["UPLOAD_FOLDER"],secure_name))
            user=User(first_name=first_name,last_name=last_name,email=email,password=generate_password_hash(password),image="image")
            Dict={
                "response":"ok",
                "first_name":first_name,
                "last_name":last_name,
                "email":email,
                "message":"you are signed in"
            }
            db.session.add(user)
            db.session.commit()
            Auth.insert(email)
            return jsonify(Dict)
        else:
            return jsonify(json_message("error","invalid email"))
    else:
       return jsonify(json_message("error","user present"))


@vote.route("/file/<filename>")
def send_the_file(filename):
    try:
        return send_from_directory(vote.config["UPLOAD_FOLDER"],filename)
    except Exception as e:
        return onError(e)
@vote.route("/logout")
def logout():
    session["logged_in"]=False
    return jsonify(json_message("ok","log out"))

@vote.route("/login",methods=['POST','GET'])
def login():
    if request.method=="GET":
        Dict={
            "response":'error',
            "message":"unsupported request method"
        }
        return jsonify(Dict)
    email=request.form["email"]
    password=request.form["password"]


    user=User.query.filter_by(email=email).first()
    if generate_password_hash(password)==user.password or 1:
        session["logged_in"]=True
        Dict={
            "response":"ok",
            "message":"successfully logged in",
            "logged_in":True
        }
        return jsonify(Dict)
    else:
        Dict={
            "response":"error",
            "user":user.email,
            "logged_in":False,
            "message":"username or password does not match"
        }

        return jsonify(Dict)

@vote.route("/create_poll",methods=['POST','GET'])
def create_poll():
    if True:
        #gets the email stored at the front end
        #gets the user
        #choices would be sent as query and number
        cache_=request.args.get("cache")
        if cache_:
            email=request.args.get("email")
            name=request.args.get("name")
            topic=request.args.get("topic")
            imagename=request.args.get("image")
            cache.new_entry(email,name,topic,0,imagename)
            return jsonify(json_message("ok","new pending option added"))
        save=None
        if request.method=="POST":
            save=request.form["save"]
        if save:
            if "file" not in request.files:
                return jsonify(json_message("error","no file selected"))
            file=request.files["file"]
            secure_name=secure_filename(file.filename)
            file.save(os.path.join(vote.config["UPLOAD_FOLDER"],secure_name))
            return  jsonify(json_message("ok","new file added"))

        email=request.args.get("email")
        user=User.query.filter_by(email=email).first()
        Topic_=request.args.get("topic")
        T=Topic(title=Topic_,count=0,users=user)
        for choice_ in cache.get_entry(email):
            T.choices.append(choice(name=choice_[0],count=0,Topic=T,imagename=choice_[3]))
        ip.new_entry(Topic_,"")
        user.topics.append(T)
        db.session.commit()
        cache.delete_entry(email)
        return jsonify(json_message("ok","you craeted a new poll"))
    else:
        return jsonify(json_message("error","not logged in"))

@vote.route("/vote")
def cast_vote():
    t_opic=request.args.get("topic")#name of topic
    person=request.args.get("person")
    load=request.args.get("load")
    vote=request.args.get("vote")
    if load:
        the_topic=Topic.query.filter_by(title=t_opic).first()#list of available topics
        if not the_topic:
            return jsonify(json_message("error","cant find this topic"))
        response={}
        x=0
        for choice_ in the_topic.choices:
            add={
                "name":choice_.name,
                "count":choice_.count,
                "imagename":choice_.imagename
                }
            response[str(x)]=add
            x+=1
        return jsonify(response)
    elif vote:
        Id=request.args.get("ip")
        if not ip.address_in_title(t_opic,Id):
            the_topic=Topic.query.filter_by(title=t_opic).first()#get the topic
            c_hoice=request.args.get("choices")#user selected choice
            for choice_e in the_topic.choices:
                if choice_e.name==c_hoice:
                    choice_e.count+=1
                    db.session.commit()
                    ip.new_entry(t_opic,Id)
                    the_topic.count+=1
                    return jsonify(json_message("ok","you just vote"))
        else:
            return jsonify(json_message("ok","you voted before"))
    else:
        return jsonify(json_message("error","invalidd parameters"))

@vote.route("/search")
def search():
    arg=request.args.get("query")
    all_topic=Topic.query.all()
    Res={}
    for topic in all_topic:
       if string_matcher(arg,topic.title):
           Dict={
               "title":topic.title,
               "choices":topic.choices
           }
           Res[topic.title]=Dict
    return jsonify(Res)

@vote.route("/profile")
def profile():
    email=request.args.get("email")
    user=User.query.filter_by(email=email).first()
    Dict={
        "first_name":user.first_name,
        "last_name":user.last_name,
        "image":user.image,
        "date":user.date_created
        }
    return jsonify(Dict)



if __name__ == "__main__":
    vote.run(debug=True)
