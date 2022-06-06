from tiwsted.internet import reactor
form twisted.internet.protocol import Protocol
form twisted.internet.protocol import ClientFactory as ClFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
IP = input("Connection IP (defaults to localhost): ")
if IP == '':
    IP = 'localhost'
class Client(Protocol):
    def dataReceive(self, data):
        data = data.decode("utf-8")
        print(data)
        self.transport.write(input("::").encode('utf-8'))

class ClientFactory(ClFactory):
    def buildProtocol(self, addr):
        return Client()

if __name__ == "__main__":
    endpoint = TCP4ClientEndpoint(reactor, IP, 6667)
    endpoint.connect(ClientFactory())
    reactor.run()
