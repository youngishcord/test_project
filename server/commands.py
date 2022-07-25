import json
import pymongo


def servmess(data):
    return f"server: {data}"


def deserialization(data):
    try:
        if data[0] == "{":
            try:
                data = json.loads(data)
            except:
                print("cant deserialize data (server)")
        else:
            print("wrong format for deserialization (server)")
        return data
    except:
        return data


def serialization(data):
    try:
        buff = json.dumps(data)
    except:
        print("cant serialize data (server)")
    if buff[0] == "{":
        return buff
    else:
        print("wrong format for serialization (server)")
        return data
