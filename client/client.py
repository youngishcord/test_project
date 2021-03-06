from email import message
from pydoc import cli
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ReconnectingClientFactory as CF
from twisted.internet.endpoints import TCP4ClientEndpoint
from config.config import HOST, PORT
import json
import messages
import pymongo




class Client(Protocol):
    def __init__(self):
        reactor.callInThread(self.send_data)
        """client = pymongo.MongoClient('localhost', 27017)
        for k in client.list_databases():
            print(k["name"])
        db = client[input("select name of DB")]
        for j in db.list_collections():
            print(j["name"])
        collection = db[input("select name of collection")]"""

    def dataReceived(self, data):
        data = data.decode()
        data = messages.deserialization(data)
        print(data)
        

    def connectionMade(self):
        print('Hello client')
        #self.transport.write(messages.conection_db())

    def send_data(self):
        while True:
            try:
                mess = input()
                if mess[0] == "!":
                    if mess == "!help":
                        self.transport.write(messages.help().encode())

                    elif mess == "!showdb":
                        self.transport.write(messages.showdb().encode())

                    elif mess == "!db":
                        self.transport.write(messages.db().encode())

                    elif mess == "!showcoll":
                        self.transport.write(messages.showcoll().encode())

                    elif mess == "!coll":
                        self.transport.write(messages.coll().encode())

                    elif mess == "!sum":
                        self.transport.write(messages.summ().encode())

                    elif mess == "!add":
                        self.transport.write(messages.add().encode())

                    elif mess == "!del":
                        self.transport.write(messages.dell().encode())

                else:
                    #print("commands start at !\ninput !help for more info")
                    self.transport.write(mess.encode())
            except:
                print("lol")



class ClientFactory(CF):
    def buildProtocol(self, addr):
        return Client()

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        CF.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print(reason)
        CF.clientConnectionLost(self, connector, reason)


if __name__ == '__main__':
    endpoint = TCP4ClientEndpoint(reactor, HOST, PORT)
    endpoint.connect(ClientFactory())
    reactor.run()