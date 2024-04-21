import pickle

class Datagrama:
    def __init__(self, id, port, table, destinationIp, destinationPort):
        self.id = id
        self.port = port
        self.routing_table = table
        self.destinationIp = destinationIp
        self.destinationPort = destinationPort

    def extractMessage(data, adress=None):
        
        objeto = pickle.loads(data)
        
        return objeto, (objeto.id, objeto.port)

    def makeMessage(self):
        
        data = pickle.dumps(self)

        return data

    def toString(self):
        return f"Roteador: ({self.id} | {self.port}) | Tabela: {self.routing_table} | DestinoIp: {self.destinationIp} | DestinoPorta: {self.destinationPort}"