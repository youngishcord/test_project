import json
from math import ceil
import pymongo


def deserialization(data):
    if data[0] == "{":
        try:
            data = json.loads(data)
        except:
            print("cant Deserialize data (client) >>")
    else:
        print("wrong format for Deserialization (client) >>")
    return data

    
def serialization(data):
    try:
        buff = json.dumps(data)
    except:
        print("cant Serialize data (client) >>")
    if buff[0] == "{":
        return buff
    else:
        print("wrong format for Serialization (client) >>")
        return data


def showdb():
    mess = {"func":"showdb"}
    return serialization(mess)

def check():
    try:
        a = int(input("create a db if there isn't one? (1/0) (standart 0) "))
        if a == 1:
            return '1'
        else:
            return '0'
    except:
        return '0'

def db():
    try:
        mess = {"func":"db",
            "name": input("input db name "), 
            "create":check()}
    except:
        mess = "db request err"
        print(mess)
        return mess
    return serialization(mess)


def showcoll():
    mess = {"func":"showcoll"}
    return serialization(mess)

def help():
    print("!sum for summation\n!add for append one doc\n!del for delete ode doc")


def summ():
    try:
        c = {"func":"sum",
            "arg1":int(input("input arg2 ")), 
            "arg2":int(input("input arg2 "))}
        print(c)
        d = json.dumps(c)
        print(type(d))
        #self.transport.write(d.encode())
    except ValueError:
        print("type except")
    except:
        print('error')
    return d


def append_one():
    pass


def del_one():
    pass