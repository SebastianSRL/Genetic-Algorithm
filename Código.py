import pandas as pd
import numpy as np
from scipy import stats
table = pd.read_excel("c:/Users/sophi/Desktop/U/Auxiliatura/DATOS.xlsx")
table.head(11)
dist_d = []
precedentes = table['Precedente']
#print(precedentes)
duracion = np.zeros((20,len(table)))
EF = np.zeros((20,len(table)))
ES = np.zeros((20,len(table)))
for j in range(19): 
  for i in range(len(table)):
    dist_r2 = 0
    dist_r1 = 0
    dist_d.append(stats.uniform(table['Duracionmed'].values[i], table['Duraciondesv'].values[i])) 
    if np.random.uniform(0,1) < table['Probriesgo1'].values[i]: 
        dist_r1 = (stats.uniform(table['Riesgo1duracionmed'].values[i], table['Riesgo1duraciondesv'].values[i])).rvs(1)
    if np.random.uniform(0,1) < table['Probriesgo2'].values[i]: 
        dist_r2 = (stats.uniform(table['Riesgo2duracionmed'].values[i], table['Riesgo2duraciondesv'].values[i])).rvs(1)
    duracion[j,i] = dist_d[i].rvs(1) + dist_r1 + dist_r2
duracion[-1,:] = np.mean(duracion[:-1,:],axis=0)
#0 es vertical, 1 horizontal
duracion = duracion.round()
#print(duracion)
for k in range(len(precedentes)):
    if precedentes[k] is np.NAN:
        EF[:,k]=0
        ES[:,k]=0
    elif isinstance(precedentes[k],int):
        ES[:,k]=EF[:,precedentes[k]]
        EF[:,k]=ES[:,k] + duracion[:,k]
    else:
        strings = [int(p) for p in precedentes[k].split(';')]
        pos = np.max(EF[:,strings],axis=1)
        ES[:,k] = pos
        EF[:,k]=ES[:,k] + duracion[:,k]
print(ES)

politicas = np.argsort(ES,axis=1)
print(politicas)
politicas = np.unique(politicas,axis=0)
print(politicas)
for _ in range(20-len(politicas)):
    tmp = np.arange(1, 11)
    np.random.shuffle(tmp)
    politicas = np.vstack([politicas, np.hstack([[0], tmp])])
print(politicas)
for j in range(20): 
  for i in range(len(table)):
    dist_r2 = 0
    dist_r1 = 0
    dist_d.append(stats.uniform(table['Duracionmed'].values[i], table['Duraciondesv'].values[i])) 
    if np.random.uniform(0,1) < table['Probriesgo1'].values[i]: 
        dist_r1 = (stats.uniform(table['Riesgo1duracionmed'].values[i], table['Riesgo1duraciondesv'].values[i])).rvs(1)
    if np.random.uniform(0,1) < table['Probriesgo2'].values[i]: 
        dist_r2 = (stats.uniform(table['Riesgo2duracionmed'].values[i], table['Riesgo2duraciondesv'].values[i])).rvs(1)
    duracion[j,i] = dist_d[i].rvs(1) + dist_r1 + dist_r2

rec_1 = 5
rec_2 = 6
done = []
prog = [0]
tiempos = [0]
Tfinal = 0
eleg = []

duracion = duracion.round()
recursos_1 = table['Recurso 1'].values
recursos_2 = table['Recurso 2'].values
print(precedentes)
for i in range(20):
    for j in range(20):
        durs = duracion[i,:]
        pol = politicas[j,:]
        while len(prog) > 0:
            id = np.argmin(tiempos) # Haya el indice del tiempo minimo (lista)
            rec_1 += recursos_1[prog[id]] 
            rec_2 += recursos_2[prog[id]]
            Tfinal += durs[prog[id]]

            done.append(prog[id])
            tiempos.pop(id)
            prog.pop(id)
        
            eleg = []
            for k, pred in enumerate(precedentes.values):
            
                if pred is np.NAN:
                    pass
                elif isinstance(pred,int):
                    if pred in done and k not in done and k not in prog: 
                        eleg.append(k)
                else:
                    strings = [int(p) for p in pred.split(';')]
                    if set(strings).issubset(set(done)) and k not in done and k not in prog:
                        eleg.append(k)

            for _, p in enumerate(pol):
                if p in eleg and rec_1 > recursos_1[p] and rec_2 > recursos_2[p]:
                    prog.append(p)
                    tiempos.append(durs[p])
                    rec_1 -= recursos_1[p]
                    rec_2 -= recursos_2[p]
            print(f"Actividad actual: {id} Actividades hechas: {done} Activdades programadas: {prog} Tiempo final: {Tfinal} Recursos [{rec_1},{rec_2}]")
        break
    break





print(duracion)

