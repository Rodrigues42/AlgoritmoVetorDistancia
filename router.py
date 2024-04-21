import socket
import threading
from datagramaInfo import Datagrama
from datagramaInfo import Canal
import time

class Roteador:
    def __init__(self, id, ip, port, numberOfRouters):
        super().__init__()
        self.id = id #identificador do roteador na rede
        self.ip = ip
        self.port = port
        self.routing_table = [[0 for i in range(numberOfRouters+1)] for j in range(numberOfRouters+1)] #tabela de roteamento
        self.neighbors = { self.id : { 'ip': self.ip, 'port': self.port, 'cust': 0 }} #vizinhos do roteador
        self.neighborsList = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket do roteador
        self.socket.bind(("127.0.0.1", port))
        self.canal = Canal()

    def receiver(self):

        while True:

            dataBytes, address = self.socket.recvfrom(1024)
            data, address = Datagrama.extractMessage(dataBytes, address)
            
            '''Mostra no console as mensagens recebidas para o roteador 1'''
            if(data.destinationPort == 10001):
                print(f"\033[93mMensagem recebida {data.toString()} do roteador ({address[0]}, {address[1]})\033[0m")
                
            '''Atualiza a tabela de roteamento e Verifica se teve mudança em sua tabela de roteamento'''
            sendNeighbor = self.update_table(data.routing_table)
            
            '''só envia a tabela de roteamento para seus vizinhos caso a sua sofreu alterações'''
            if sendNeighbor:
                for neighbor in self.neighbors:
                    self.sender(self.neighbors[neighbor]["ip"], self.neighbors[neighbor]["port"])
        
    def sender(self, destinationIp=None, destinationPort=None):

        if destinationIp == None and destinationPort == None:
            for chave, valor in self.neighbors.items():
                if valor['port'] != self.port:
                    datagrama = Datagrama(self.id, self.port, self.routing_table, valor['ip'], valor['port'])
                    self.canal.sendPackage(self.socket, datagrama, (valor['ip'], valor['port']))

                    '''Mostra no console as mensagens enviadas para os vizinhos do roteador 1'''
                    if(int(self.id) == 1):
                        print(f"\033[92mEnviando mensagem {datagrama.toString()} para roteador ('{valor['ip']}', {valor['port']})\033[0m")
        else:
            if destinationPort != self.port:
                datagrama = Datagrama(self.id, self.port, self.routing_table, destinationIp, destinationPort)
                
                self.canal.sendPackage(self.socket, datagrama, (destinationIp, destinationPort))
                
                '''Mostra no console as mensagens enviadas para os vizinhos do roteador 1'''
                if(int(self.id) == 1):
                    print(f"\033[92mEnviando mensagem {datagrama.toString()} para roteador {(destinationIp, destinationPort)}\033[0m")

    def update_table(self, neighbor_table):

        change = False

        num_routers = len(self.routing_table) - 1

        for x in range(num_routers + 1):
            if self.routing_table[x][0] == int(self.id):
                posicao = x

        # Atualiza a tabela de roteamento com base nas informações do vizinho
        for i in range(num_routers + 1):
            if neighbor_table[i][0] in self.neighborsList:
                for j in range(1, num_routers + 1):
                    if neighbor_table[0][j] in self.neighborsList:
                        if neighbor_table[i][0] != neighbor_table[0][j] and neighbor_table[i][j] != 0:
                            if self.routing_table[i][j] == 0:
                                if self.routing_table[posicao][j] > neighbor_table[i][j] + neighbor_table[i][posicao]:
                                    self.routing_table[posicao][j] = neighbor_table[i][j] + neighbor_table[i][posicao]
                                
                                self.routing_table[i][j] = neighbor_table[i][j]
                                change = True

                                if self.id == '1' and i-1 == 1:
                                    self.printRoutingTable(i-1, j)

                            else:
                                if self.routing_table[i][j] > neighbor_table[i][j]:
                                    self.routing_table[i][j] = neighbor_table[i][j]
                                    if self.id == '1':
                                        self.printRoutingTable(i, j)
                    else:
                        self.routing_table[i][j] = neighbor_table[i][j]

        #print(self.routing_table)

        return change      

    # adiciona vizinhos com base na matriz de adjacência
    def addNeighborAndRoutingTable(self, table):

        # Preencha a primeira linha com números sequenciais de 0 a n-1
        for i in range(len(table)):
            self.routing_table[0][i] = i

        # Preencha a primeira coluna com números sequenciais de 0 a n-1
        for i in range(len(table)):
            self.routing_table[i][0] = i

        for i in range(1, len(table)):
            if table[i][0] == int(self.id):
                self.routing_table[i][0] = int(self.id)
                for j in range(1, len(table)):
                    self.routing_table[0][j] = table[0][j]
                    if table[i][j] != 0:
                        self.neighbors[f"{table[0][j]}"] = { 'ip': "127.0.0.1", 'cust': table[i][j], 'port': 10000 + int(table[0][j]) }
                        self.neighborsList.append(table[0][j])
                        self.routing_table[i][j] = table[i][j]
                    else:
                        self.routing_table[i][j] = table[i][j]
            else:
                self.routing_table[i][0] = table[i][0]

    def printRoutingTable(self, linhaX=None, colunaY=None):
        
        print("--" * 50)
        print(f"Rotedor {self.id}")
        print("--" * 50)
        
        for i in range(len(self.routing_table)):
            for j in range(len(self.routing_table)):
                if i == linhaX and j == colunaY:
                    print(f"\033[91m{self.routing_table[i][j]:15}\033[0m", end=" | ")
                else:
                    print(f"{self.routing_table[i][j]:15}", end=" | ")
            print()
        print("--" * 50)  

    def printNeighbors(self):
        print(self.neighbors)        

    def init(self, adjacencyMatrix):
        self.addNeighborAndRoutingTable(adjacencyMatrix)
        self.printRoutingTable()
    
    def run(self):
        thread = threading.Thread(target=self.receiver)
        thread.daemon = True
        thread.start()
