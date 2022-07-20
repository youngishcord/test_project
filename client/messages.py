import json
import pymongo


def deserialization(data):
    if data[0] == "{":
        try:
            data = json.loads(data)
        except:
            print("cant deserialize data")
    else:
        print("wrong format for deserialization")
    return data

    
def serialization(data):
    try:
        buff = json.dumps(data)
    except:
        print("cant serialize data")
    if buff[0] == "{":
        return buff
    else:
        print("wrong format for serialization")
        return data


def connection_db():
    connect_message = 0


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