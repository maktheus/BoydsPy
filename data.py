import numpy as np
import pandas as pd
from datetime import datetime
infecteds = 0
healthies = 0
curado =0
dead =0
data_infectados=[]
data_saudaveis = []
data_curados=[]
data_mortos=[]

#array = np.array([0,30,0,0])

class Data():
   
    def count(flock):
        global infecteds, healthies,data,curado,dead,array
        # datetime object containing current date and time
        # dd/mm/YY H:M:S
        for boid in flock:
          
            if boid.infected == True and boid.curado == False and boid.alive == True:
                infecteds += 1
            elif boid.infected == False and boid.curado == False and boid.alive == True:
                healthies += 1
            elif boid.curado == True and boid.alive == True:
                curado +=1
            elif boid.alive == False:
                dead += 1

        data_infectados.append(infecteds)
        data_saudaveis.append(healthies)
        data_curados.append(curado)
        data_mortos.append(dead)
        array = np.array(data_saudaveis)

        #array = np.append([data],axis=0)
        graphic = pd.DataFrame({
            "Saudaveis":data_saudaveis,
            "Infectados":data_infectados,
            "Mortos":data_mortos,
            "Curados":data_curados,
            })
        graphic.to_csv('Teste.csv',index=False)
        #print(graphic)
        # datanow = np.array([infecteds, healthies])
        # data.append(datanow)
        infecteds = 0
        healthies = 0
        curado =0
        dead = 0