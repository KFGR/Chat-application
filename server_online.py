import soket
class Server:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.server.bind((self.host,self.port))
        print(self.host)

    def get_data(self):
        data, address = self.server.recvfrom(128)
        return data.decode(), address


    def forward_info(self, clients,address):
        listen = self.string_format(clients).encode()
        for peer in clients:

            for add in address:
                self.server.sendto(listen,add)


    def string_format(self,clients):
        out = [str(items) for index in clients for items in index]
        listenformat = ' '.join(out)
        return listenformat

    def appendd_clients(self, clients, data, address):
        clients.append((address[0],data[1]))
        self.server.sendto(b'ready', address)


    def popp_clients(self,clients, index):
        clients.pop(index)






def main():
    server = Server('64.227.18.224', 40000)
    Clients = []
    all_add = []

    while True:
        print("clients are: ", Clients)
        data, address = server.get_data()

        if data.find('|') == -1:
            messages = 'M' + data
            for i in all_add:
                server.server.sendto(str(messages).encode(), i)



        data = data.split('|')
        all_add.append(address)
        print("data in main: ", data)
        print("address in main: ", address)

        if 'join' == data[0]:
            server.appendd_clients(Clients, data, address)
            server.forward_info(Clients,all_add)
        if 'leave' == data[0]:
            for index,item in enumerate(Clients):
                if item[0] == address[0]:
                    server.popp_clients(Clients,index)
                    server.forward_info(Clients,all_add)
                    break


main()
