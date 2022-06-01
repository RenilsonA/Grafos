import numpy as np

occupancy = np.ones((10, 10))
occupancy[0:5, 0] = np.inf
occupancy[5, 0:5] = np.inf
occupancy[5:8, 5] = np.inf
occupancy[0:3, 5:8] = np.inf
occupancy[7:9, 3] = np.inf
occupancy[5:10, 8] = np.inf

robot_pos_c = [9, 0] # Robot current position
robot_pos_d = [0, 2] # Robot desired position
#for i in range(10):
    #for j in range(10):
      #if occupancy[9-i, j] == 1:
        #path.append(locaisVolta(9-i, j))

def robot_path(robot_pos, robot_pos_d, occupancy):
  path = []
  
  def locaisVolta(local):
    pisos = []
    i, j = local
    if i+1 < 10 and occupancy[i+1, j] < np.inf:
      pisos.append((i+1, j))
    if i-1 >= 0 and occupancy[i-1, j] < np.inf:
      pisos.append((i-1, j))
    if j+1 < 10 and occupancy[i, j+1] < np.inf:
      pisos.append((i, j+1))
    if j-1 >= 0 and occupancy[i, j-1] < np.inf:
      pisos.append((i, j-1))
    return pisos

  def buscaLargura():
    visitar = [robot_pos]
    visitados = [robot_pos]
    caminhos = dict()
    while len(visitar) > 0:
      local = visitar[0]
      del visitar[0]
      for teste in locaisVolta(local):
        if teste not in visitados:
          visitados.append(teste)
          caminhos[str(teste[0])+", "+str(teste[1])] = local
          if teste[0] == robot_pos_d[0] and teste[1] == robot_pos_d[1]:
            caminho = []
            passo = teste
            while passo != robot_pos:
              caminho.append(passo)
              passo = caminhos[str(passo[0])+", "+str(passo[1])]
            caminho.append(robot_pos)
            caminho.reverse()
            return caminho
          else:
            visitar.append(teste)
    return -1

  path = buscaLargura()
  return path

path = robot_path(robot_pos_c, robot_pos_d, occupancy)
print(path)