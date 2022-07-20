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
