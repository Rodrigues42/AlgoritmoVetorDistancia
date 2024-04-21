import time
from router import Roteador

'''Faz a leitura da matriz de adjacência com a topologia inicial dos roteadores'''
caminho_arquivo = 'matriz.txt'
matrizAdjacencia = []

with open(caminho_arquivo, 'r') as arquivo:
    for linha in arquivo:
        matrizAdjacencia.append([int(numero) for numero in linha.split()])

numberOfRouters = len(matrizAdjacencia[0])-1
roteadores = []
port = 10001


'''Instancia cada roteador em um processo diferente com sua respectiva porta'''
print("--" * 50)
print("Configuração inicial Roteadores")
print("--" * 50)
for i in range(numberOfRouters):

    roteador = Roteador(f"{i+1}", "127.0.0.1", port, numberOfRouters) # substituir pelo IP do roteador
    roteadores.append(roteador)
    port += 1

    roteador.init(matrizAdjacencia)
    roteador.run()

for roteador in roteadores:
    roteador.sender()
    

time.sleep(20)


''' Mostra a tabela de roteamento final de cada roteador'''
print("--" * 50)
print("Configuração Final Roteadores")
print("--" * 50)
for roteador in roteadores:

    roteador.printRoutingTable()