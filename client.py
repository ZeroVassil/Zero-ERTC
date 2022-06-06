from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ReconnectingClientFactory as ClFactory
from twisted.internet.endpoints import TCP4ClientEndpoint




#Client functions
def fHelp():
    print('''
All client side commands start with "$" for example if you want to disconnect from a server you'd use "$disconnect" or "$dc" for short

-----------------------------------------------------------------
                  Client side command list :
-----------------------------------------------------------------
$help                   > lists all commands
$connect <IP>           > initiates connection with specified IP
$disconnect             > disconnects from server (if connected)
$username <username>    > sets or overwrites username
                          using $username $destroy will clear
                          current username
$serverinfo             > attempts to get info for currently
                          connected server (only works if server
                          is configured to return information)
$exit                   > disconnects from server and end client
    ''')




#Initial loop
print('use "$help" to get you started.')
while True:
    command = input(":: ").lower()
    if command == "$help":
        fHelp()
    elif command.split(" ")[0] == "$connect" or command.split(" ")[0] == "$con":
        try:
            IP = command.split(" ")[1]
            break
        except:
            print("[!] Wrong syntax use $connect <IP>")
            
    elif command.split(" ")[0] == "$username":
        if command.split(" ")[1] == "$destroy":
            print("[!] Cleared username")
            with open("client.username", "w") as f:
                f.write("")
        else:
            username = command.split(" ")[1]
            with open("client.username", "w") as f:
                f.write(username)
            print("[!] username set to " + username)
    elif command == "$exit":
        exit()
    elif command == "$disconnect" or command == "$dc":
        print("[!] You are not currently connected to any servers")
    elif command == "$serverinfo" or command == "$si":
        print("[!] You are not currently connected to any servers")
    else:
        print("[!] Unknown command")
try:
    with open("client.username", "r") as f:
        nickname = f.read()
except:
    nickname = ""

if nickname == "":
    print("You haven't setted up a permanent username yet")
    print("if you want to use 1 time username please enter your username")
    print("or if you want to setup permanent nickname type $username followed by your username")
    print("(Example:   :: $username myUserName   or   :: myUserName)")
    username = input(":: ")
    try:
        if username.split(" ")[0] == "$username":
            with open("client.username", "w") as f:
                f.write(username.split(" ")[1])
        else:
            nickname = username
    except:
        print("Unknown error accoured (errCode:10)")
        exit()

class Client(Protocol):
    def __init__(self):
        reactor.callInThread(self.sendData)

    def connectionMade(self):
        self.transport.write(nickname.encode("utf-8"))

    def dataReceived(self, data):
        data = data.decode("utf-8")
        print(data)

    def sendData(self):
        while True:
            self.transport.write(input("").encode('utf-8'))


class ClientFactory(ClFactory):
    def buildProtocol(self, addr):
        return Client()

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        ClFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print(reason)
        ClFactory.clientConnectionLost(self, connector, reason)

if __name__ == "__main__":
    endpoint = TCP4ClientEndpoint(reactor, IP, 6667)
    endpoint.connect(ClientFactory())
    reactor.run()
