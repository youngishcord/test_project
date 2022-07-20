from bson import encode
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.protocol import ServerFactory as SF
from twisted.internet.endpoints import TCP4ServerEndpoint
from config.config import PORT
import json
import pymongo
import commands


class Server(Protocol):

    def __init__(self):
        print("initialization")
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = None
        self.collection = None
        '''w = [i for i in client.list_databases()]
        q = json.dumps({'db' : w})
        print(q)
        self.transport.write(q.encode())'''

    
    def connectionMade(self):
        print(f'New connection from {self}')
        self.transport.write('Connected\n'.encode())
    
    
    def dataReceived(self, data):
        data = data.decode()
        data = commands.deserialization(data)
        print(data)
        print(type(data))
        
        if type(data) == "dict":
        
            if self.db == None or self.collection == None:
                db_names = [i["name"] for i in self.client.list_databases()]
                q = f"select DB\n{json.dumps(db_names)}"
                print(q)
                collection_names = [j["name"] for j in self.db.list_collections()]
                self.transport.write(q.encode())
        

            try:
                if data["func"] == "sum":
                    #print(data["arg1"])
                    self.transport.write(summation(data["arg1"], data["arg2"]))
            except:
                print("wrong value")
        else:
            self.transport.write(data.encode())


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