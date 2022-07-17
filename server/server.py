from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.protocol import ServerFactory as SF
from twisted.internet.endpoints import TCP4ServerEndpoint
from config.config import PORT
import json

class Server(Protocol):
    def __init__(self):
        print("initialization")

    def connectionMade(self):
        print(f'New connection from {self}')
        self.transport.write('Connected'.encode())

    def dataReceived(self, data):
        data = data.decode()
        print(data)
        print(type(data))
        try:
            data = json.loads(data)
            print(data)
            print(type(data))
            if data["func"] == "sum":
                print(data["arg1"])
                summation(data["arg1"], data["arg2"])
        except:
            print("wrong value")

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