import socket
import sys
import threading
import time
class Peers:
    def __init__(self):
        """Constructor, initializes an object from Class Peers"""
        self.peer_port = 50000
        self.server_port = 40000
        #self.hostname = socket.gethostname()
        self.messages = []
        #print(self.hostname, type(self.hostname))

        self.server_ip = input('IP: ')
        self.rendezvous_server = (self.server_ip, self.server_port)
        self.rendezvous_peer = ('0.0.0.0', self.peer_port)

        #create new socket and bind to rendezvous_server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('0.0.0.0', self.server_port))

        #create new socket and bind to rendezvous_peer
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peer_socket.bind(('0.0.0.0', self.peer_port))

        #connect server and receive peers data into a touple ((),())
        self.dataList = self.server_connect()
        #print("datalist: ", self.dataList)


        #self.peer_list = self.data_to_touple(self.dataList)
        self.peer_list = self.data_to_touple(self.dataList)
        # #Creating threads so that the port is able to listen for the server
        self.server_listen = threading.Thread(target=lambda: self.listen_server(), daemon=True)#threading(self.listen_server())
        self.server_listen.start()

        #Creating threads so that the port is able to listen for peers
        self.peers_listen = threading.Thread(target=lambda: self.listen_peers(), daemon=True)#threading(self.listen_peers())
        self.peers_listen.start()
        #print('mensajes en main: ',self.messages)
        #print(self.dataList)




    def get_localIP(self):
        """Function that returns the local IP of a peer"""
        hostname = socket.gethostname()
        local_IP = socket.gethostbyname(hostname)
        #print('hostname is {}, and ip of hostname is {}'.format(hostname, local_IP))
        return local_IP

    def server_connect(self):
        """Function to connect to the server while receiving list of peers in string data
        Also ask for username when connecting"""
        self.user = input('Enter username: ')
        message = f'join|{self.user}'
        #print("message in connect: ", type(message))
        self.server_socket.sendto(message.encode(), self.rendezvous_server)
        while True:
            data, address = self.server_socket.recvfrom(1024)
            if data.decode().strip()=='ready':
                #print("data decode in if: ", data.decode())
                break
        data, address = self.server_socket.recvfrom(1024) #data is bytes
        #print("data and address at end of connect: ", type(data), data, address)
        return data.decode()

    def listen_peers(self):
        """Function to listen to peers socket, this function is always running"""
        while True:
            data, address = self.peer_socket.recvfrom(1024)
            #print("data {}, y direccion {}, recibida en listen_server".format(data.decode(), address))
            if address[0] != self.get_localIP():
                for peer in self.peer_list:
                #    print("peer {}, address {}".format(peer,address))
                    if peer[0] == address[0]:
                        self.user = peer[1]
                        break
                self.messages.append('{}:{}'.format(self.user,data.decode()))
                print("mesajes: ", self.messages)


    def listen_server(self):
        """Function to listen to server socket, adds clients or peers to the list as an array of tuples"""
        while True:
            data, address = self.server_socket.recvfrom(1024)

            if str(data.decode())[0] == 'M':
                #print('this is a message')
                self.messages.append(str(data[1:].decode()))

            else:
                #print('this is a client')
                self.peer_list.clear()
                self.peer_list.extend(self.data_to_touple(data.decode())) #adds clients with IP [(IP,USERNAME),...]
                print("peers ", self.peer_list)



    def peer_exit(self):
        """Function to send informatino to another peer when someone has exit the chat"""
        txt = f'leave|'
        self.server_socket.sendto(txt.encode(), self.rendezvous_server)

    def data_to_touple(self, data):
        """Function to convert the string data into an array of touples ((),())"""
        decoded = data
        decoded_list = list(decoded.split(' '))
        iterator = iter(decoded_list)
        decoded_touple = zip(iterator,iterator)
        return list(decoded_touple)

    def recv(self):
        a, b = self.peer_socket.recvfrom(1024)
        return a, b

    def send_information(self, txt):
        """Function to send messages and answers to other peers"""
        #self.messages.append(txt) #['mensaje', 'user:[mensaje]']
        self.peer_socket.sendto(txt.encode(), (self.server_ip, self.server_port))
        print("mensajes enviados en send information: ", self.messages)


    def threading(self, function):
        """Function to create threads in order for the ports to listen to either server or peers"""
        return threading.Thread(target=lambda: function, daemon=True)

if __name__ == '__name__':
    peer = Peers()


"""fucnion en el servidor que envie la data que recibe cada mensaje enviado al servidor sendto(mensaje, (ip,port))
en el servidor
while true:
    recvfrom()
    sendto(all peers)"""
