from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ReconnectingClientFactory as CF
from twisted.internet.endpoints import TCP4ClientEndpoint
from config import HOST, PORT

class Client(Protocol):
    def __init__(self):
        reactor.callInThread(self.send_data)

    def dataReceived(self, data):
        data = data.decode()
        print(data)

    def connectionMade(self):
        print('Hello client')

    def send_data(self):
        while True:
            self.transport.write(input().encode())



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