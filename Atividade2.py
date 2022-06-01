import numpy as np

occupancy = 10 * np.random.rand(10, 10)
occupancy[0:5, 0] = np.inf
occupancy[5, 0:5] = np.inf
occupancy[5:8, 5] = np.inf
occupancy[0:3, 5:8] = np.inf
occupancy[7:9, 3] = np.inf
occupancy[5:10, 8] = np.inf

robot_pos_c = [9, 0] # Robot current position
robot_pos_d = [0, 2] # Robot desired position

def robot_path(robot_pos, robot_pos_d, occupancy):
    path = []

    '''
    Criei um grafo pois acho melhor de visualizar e manusear
    Abaixo, tem a classe grafo para criar um nó e vertices
    '''
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
    
    '''
    Algoritmo de dijkstra para testar todos caminhos possíveis
    Escolhe o caminho que o peso (conteúdo de B que vai de A -> B e
    o peso de B -> A é o conteúdo de A) total for menor
    '''
    def dijkstra(grafo, de, para):
        caminho = {de: (None, 0)}
        NoAtual = de
        visitados = set()
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
            NoAtual = proximoNo
        path.reverse()
        return path

    grafo = grafo()

    '''
    Checa os vizinhos válidos como passagem, adicionando no grafo nos
    dois sentidos, cada número de nó vai de 0 a 99, onde é definido pela equação
    (10*(linha) + coluna), adicionando no gráfo todos os nós possíveis, ignorando
    apenas os nós infinitos, logo tem menos de 100 nós.
    '''
    def locaisVolta(local):
        i, j = local
        if i+1 < 10 and occupancy[i+1, j] < np.inf:
            grafo.addVertice((10*i)+j, (10*(i+1))+j, occupancy[i+1][j])
            grafo.addVertice((10*(i+1))+j, (10*i)+j, occupancy[i][j])
        if i-1 >= 0 and occupancy[i-1, j] < np.inf:
            grafo.addVertice((10*i)+j, (10*(i-1))+j, occupancy[i-1][j])
            grafo.addVertice((10*(i-1))+j, (10*i)+j, occupancy[i][j])
        if j+1 < 10 and occupancy[i, j+1] < np.inf:
            grafo.addVertice((10*i)+j, (10*i)+j+1, occupancy[i][j+1])
            grafo.addVertice((10*i)+j+1, (10*i)+j, occupancy[i][j])
        if j-1 >= 0 and occupancy[i, j-1] < np.inf:
            grafo.addVertice((10*i)+j, (10*i)+j-1, occupancy[i][j-1])
            grafo.addVertice((10*i)+j-1, (10*i)+j, occupancy[i][j])

    '''
    Percorre toda a matriz, checa se o local é válido, e se sim,
    checa seus vizinhos verticais e horizontais, e se for válido
    adiciona no grafo
    '''
    for i in range(10):
        for j in range(10):
            if occupancy[i, j] < np.inf:
                locaisVolta((i, j))
    
    '''
    Chama a funcão dijkstra. com grafo iniciado, que vai do nó 90 ao 1
    (com base nas coordenadas disponibilizadas por robot_pos_c e robot_pos_d)
    '''
    path = dijkstra(grafo, 10*robot_pos_c[0]+robot_pos_c[1], 10*robot_pos_d[0]+robot_pos_d[1])
    return path

path = robot_path(robot_pos_c, robot_pos_d, occupancy)
print(path)