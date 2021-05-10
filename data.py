import numpy as np
import pandas as pd
from datetime import datetime
infecteds = 0
healthies = 0
data=[]
class Data():
   
    def count(flock):
        global infecteds, healthies,data
        # datetime object containing current date and time
        # dd/mm/YY H:M:S
        for boid in flock:
            if boid.infected == True:
                infecteds += 1
            elif boid.infected == False and self.curado == False:
                healthies += 1
        datanow = np.array([infecteds, healthies])
        data.append(datanow)
              
        infecteds = 0
        healthies = 0