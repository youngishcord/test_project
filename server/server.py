from bson import encode
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.protocol import ServerFactory as SF
from twisted.internet.endpoints import TCP4ServerEndpoint
from config.config import PORT
import json
import pymongo
import commands
from commands import servmess


class Server(Protocol):

    def __init__(self):
        print("initialization")
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = None
        self.collection = None
        self.db_names = None
        self.coll_names = None
        

    
    def connectionMade(self):
        print(f'New connection from {self}')
        self.transport.write('Connected\n'.encode())
        #self.transport.write(f"db - {self.db}\n".encode())
        #self.transport.write(f'collection - {self.collection}\n'.encode())
        #self.transport.write('select db\n'.encode())
        '''db_names = [i["name"] for i in self.client.list_databases()]
        q = f"select DB\n{json.dumps(db_names)}"
        print(q)
        self.transport.write(q.encode())'''
        self.show_db()
        
    
    
    def dataReceived(self, data):
        data = data.decode()
        data = commands.deserialization(data)
        print(data)
        print(type(data))
        try:
            if isinstance(data, dict) :
            
                '''if self.db == None or self.collection == None:
                    db_names = [i["name"] for i in self.client.list_databases()]
                    q = f"select DB\n{json.dumps(db_names)}"
                    print(q)
                    collection_names = [j["name"] for j in self.db.list_collections()]
                    self.transport.write(q.encode())'''

                try:
                    if data["func"] == "sum":
                        #print(data["arg1"])
                        self.transport.write(summation(data["arg1"], data["arg2"]))
                    elif data["func"] == "showdb":
                        self.show_db()
                    elif data["func"] == "db":
                        self.select_db(data)
                    elif data["func"] == "showcoll":
                        self.show_coll()
                    elif data["func"] == "coll":
                        self.select_coll(data)
                    elif data['func'] == "help":
                        self.help()
                    elif data['func'] == "add":
                        self.insert_doc(data['body'])
                    elif data['func'] == "del":
                        self.delete_doc(data['body'])
                except:
                    print(servmess("wrong 'func' name"))
            else:
                self.transport.write(servmess(data).encode())
        except:
            print("message MISSTAKE")
            self.transport.write(servmess("message MISSTAKE").encode())


    def show_db(self):
        print('show db called')
        self.db_names = [i["name"] for i in self.client.list_databases()]
        #q = f"DBs : {json.dumps(self.db_names)}"
        q = f"DBs : {commands.serialization(self.db_names)}"
        print(q)
        self.transport.write(q.encode())
        
    def select_db(self, data):
        print("select db called")
        try:
            if data["create"] == "0":
                if data["name"] not in self.db_names:
                    print(servmess(f"{data['name']} not in dbs"))
                    self.transport.write(servmess(f"{data['name']} not in dbs\n").encode())
                    return
                else:
                    self.db = self.client[data["name"]]
            else:
                self.db = self.client[data["name"]]
            self.transport.write(servmess(f"current db {self.db.name}\n").encode())
            self.show_coll()

        except:
            print("select db MISSTAKE")
            self.transport.write(servmess("select db MISSTAKE").encode())


    def show_coll(self):
        try:
            if self.db == None:
                print(servmess(f"db is {self.db}, select db"))
                self.transport.write(servmess(f"db is {self.db}, select db".encode()))
            else:
                if self.db.name not in self.db_names:
                    print(servmess("empty db"))
                    self.transport.write(servmess("empty db").encode())
                    self.coll_names = "empty"
                else:
                    self.coll_names = [j["name"] for j in self.db.list_collections()]
                    q = f"Collections : {json.dumps(self.coll_names)}"
                    print(q)
                    self.transport.write(q.encode())
        except:
            print("show_coll MISSTAKE")
            self.transport.write(servmess("show_coll MISSTAKE").encode())

    def select_coll(self, data):
        try:
            if data["create"] == "0":
                if self.coll_names == "empty":
                    print(servmess('collection empty'))
                    self.transport.write(servmess("collection empty\n").encode())
                    return
                if data['name'] not in self.coll_names:
                    print(servmess(f"{data['name']} not in collections"))
                    self.transport.write(servmess(f"{data['name']} not in collections\n").encode())
                    return
                else:
                    self.collection = self.db[data['name']]
            else:
                self.collection = self.db[data['name']]
        except:
            print("select_coll MISSTAKE")
            self.transport.write(servmess("select_coll MISSTAKE").encode())


    def insert_doc(self, data):
        try:
            data = commands.deserialization(data)
            if self.collection != None:
                return self.collection.insert_one(data).inserted_id
            else:
                print("collection not selected")
                self.transport.write(servmess("collection not selected").encode())
        except:
            print('cant insert')
            self.transport.write(servmess("insert MISSTAKE").encode())

    def delete_doc(self, data):
        try:
            data = commands.deserialization(data)
            if self.collection != None:
                return self.collection.delete_one(data)
            else:
                print("collection not selected")
                self.transport.write(servmess("collection not selected").encode())
        except:
            print('cant delete')
            self.transport.write(servmess("delete MISSTAKE").encode())


    def help(self):
        print(servmess('''!help
    !showdb
    !showcoll
    !db for select db
    !coll for select collection
    !add for insert doc
    or use {"func": "add","body":{.....}}
    !del for delete doc
    or use {"func": "del","body":{.....}}
    ''').encode())

        self.transport.write(servmess('''!help
    !showdb
    !showcoll
    !db for select db
    !coll for select collection
    !add for insert doc
    or use {"func": "add","body":{.....}}
    !del for delete doc
    or use {"func": "del","body":{.....}}
    ''').encode())

        
    def connectionLost(self, reason):
        print(f"connectoin lost <{self}>,\n{reason}")


class ServerFactory(SF):
    def __init__(self):
        print("start server")
        #self.user = self

    def buildProtocol(self, addr):
        return Server()


def summation(arg1, arg2):
    print(f"сумма {arg1} + {arg2} = {arg1 + arg2}")
    return arg1 + arg2


if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, PORT)
    endpoint.listen(ServerFactory())
    reactor.run()