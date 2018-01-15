import json

class Cache(object):
    """This cache request i.e when creating a new poll users
        can create multiple choice
    """
    def create_json(self):
        with open("cache.json","w") as f:
            f.write("{}")

    def new_entry(self,user,name,topic,count,imagename):
        Dict=json.loads(open("/home/haibeeyy/mysite/cache.json").read())
        if user in Dict:
            Dict[user].append([name,topic,count,imagename])
        else:
            Dict[user]=[[name,topic,count,imagename]]
        with open("/home/haibeeyy/mysite/cache.json","w") as f:
            f.write(json.dumps(Dict))

    def delete_entry(self,user):
        Dict=json.loads(open("/home/haibeeyy/mysite/cache.json").read())
        try:
            Dict.pop(user)
        except KeyError:
            return False
        with open("/home/haibeeyy/mysite/cache.json","w") as f:
            f.write(json.dumps(Dict))
        return True

    def get_entry(self,name):
        Dict=json.loads(open("/home/haibeeyy/mysite/cache.json").read())
        if name in Dict:
            return Dict[name]

class Ip(object):
    def create_json(self):
        with open("ip.json","w") as f:
            f.write("{}")

    def new_entry(self,title,address):
        Dict=json.loads(open("/home/haibeeyy/mysite/ip.json").read())
        if title in Dict:
            Dict[title].append(address)
        else:
            Dict[user]=[address]
        with open("/home/haibeeyy/mysite/ip.json","w") as f:
            f.write(json.dumps(Dict))

    def delete_entry(self,user):
        Dict=json.loads(open("/home/haibeeyy/mysite/ip.json").read())
        try:
            Dict.pop(user)
        except KeyError:
            return False
        with open("/home/haibeeyy/mysite/ip.json","w") as f:
            f.write(json.dumps(Dict))
        return True

    def get_entry(self,name):
        Dict=json.loads(open("/home/haibeeyy/mysite/ip.json").read())
        if name in Dict:
            return Dict[name]
    def address_in_title(self,title,adress):
         Dict=json.loads(open("/home/haibeeyy/mysite/ip.json").read())
         return adress in Dict[title]