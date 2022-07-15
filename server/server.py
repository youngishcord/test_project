from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.protocol import ServerFactory as SF
from twisted.internet.endpoints import TCP4ServerEndpoint
from config.config import PORT

class Server(Protocol):
    def __init__(self):
        print("initialization")

    def connectionMade(self):
        print(f'New connection from {self}')
        self.transport.write('Connected'.encode())

    def dataReceived(self, data):
        data = data.decode()
        print(data)

class ServerFactory(SF):
    def __init__(self):
        print("start server")
        #self.user = self

    def buildProtocol(self, addr):
        return Server()


if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, PORT)
    endpoint.listen(ServerFactory())
    reactor.run()