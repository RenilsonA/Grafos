import string
import numpy as np

class grafo:
    def __init__(self):
        from collections import defaultdict
        self.vertices = defaultdict(list)
        self.pesos = {}
    def addVertice(self, de, para, peso):
        self.vertices[de].append(para)
        self.vertices[para].append(de)
        self.pesos[(de, para)] = peso
        self.pesos[(para, de)] = peso

def dijkstra(grafo, de, para):
    caminho = {de: (None, 0)}
    NoAtual = de
    visitados = set()
    total = 0
    while NoAtual != para:
        visitados.add(NoAtual)
        destinos = grafo.vertices[NoAtual]
        pesoPCaminhoAtual = caminho[NoAtual][1]
        for proximoNo in destinos:
            peso = grafo.pesos[(NoAtual, proximoNo)] + pesoPCaminhoAtual
            if proximoNo not in caminho:
                caminho[proximoNo] = (NoAtual, peso)
            else:
                MenorPeso = caminho[proximoNo][1]
                if MenorPeso > peso:
                    caminho[proximoNo] = (NoAtual, peso)
        proximoDest = {no: caminho[no] for no in caminho if no not in visitados}
        NoAtual = min(proximoDest, key=lambda k: proximoDest[k][1])
    path = []
    while NoAtual is not None:
        path.append(NoAtual)
        proximoNo = caminho[NoAtual][0]
        if proximoNo is not None:
            total += grafo.pesos[(proximoNo, NoAtual)]
        NoAtual = proximoNo
    path.reverse()
    return path, total


G = grafo()
f = open('https://drive.google.com/file/d/1U_b0vtRgq42IX4s814Ei_5uZNDptCkea/view', 'r')
a = 0
for i in f:
    if a > 0:
        x = i.split()
        G.addVertice(int(x[0]), int(x[1]), int(x[2]))
        G.addVertice(int(x[1]), int(x[0]), int(x[2]))
    a += 1
f.close()

def gerar_tabela_dist(G):
    D = np.zeros((12,12)) # Alterar
    for i in range(13):
        for j in range(13):
            if i != j and i > 0 and j > 0:
                f, total = dijkstra(G, i, j)
                print(f, total)
                for k in f:
                    if k != f[0] and D[f[0] - 1, k - 1] == 0:
                        D[f[0] - 1, k - 1] = total
                        D[k - 1, f[0] - 1] = total
    return D

D = gerar_tabela_dist(G)
print(D)
