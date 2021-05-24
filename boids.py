import random
from p5 import *
from numpy.random import default_rng
import numpy as np
frames=0
daystartofusingmask=0
class Boid():
    
    def __init__(self, x, y, width, height,infected,curado,alive):
        self.position = Vector(x, y)
        vec = (np.random.rand(2) - 0.5)*10
        self.velocity = Vector(*vec)
        vec = (np.random.rand(2) - 0.5)/2

        self.acceleration = Vector(*vec)
        self.max_force = 0.3
        self.max_speed = 5
        self.perception = 120
        self.size =8
        
        #Flags
        self.curado = curado
        self.alive = alive
        self.infected= infected
        self.usingmask = False
        #Days
        self.days =0
        self.width = width
        self.height = height
     


    def update(self):
        global frames
        frames+=1
        if self.alive == True:
            self.velocity += self.acceleration
            self.position += self.velocity
            #print(self.position)
            #limit
            if np.linalg.norm(self.velocity) > self.max_speed:
                self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed
            self.acceleration = Vector(*np.zeros(2))

    def show(self):
        stroke(255)
        if self.infected == False and self.alive == True and self.curado== False and self.usingmask == False:
            #blue
            fill(0, 0, 255)
            circle((self.position.x, self.position.y), self.size,mode=None)

        if self.infected == False and self.alive == True and self.curado== False and self.usingmask == True:
            #Mascara AZUL
            fill(0, 0, 255)
            circle((self.position.x, self.position.y), self.size,mode=None)
            fill(255, 255, 255)
            circle((self.position.x, self.position.y+1), 6,mode=None)

        elif self.infected == True and self.alive == True and self.curado == False and self.usingmask== False: 
            #red
            fill(255, 0, 0)
            circle((self.position.x, self.position.y), self.size,mode=None)

        elif self.infected == True and self.alive == True and self.curado == False and self.usingmask == True:
            #red with mask
            fill(255, 0, 0)
            circle((self.position.x, self.position.y), self.size,mode=None)
            fill(255, 255, 255)
            circle((self.position.x, self.position.y+1), 6,mode=None)


        elif self.alive == False:
            #Dead
            fill(128, 128, 128)
            circle((self.position.x, self.position.y), self.size,mode=None)

        elif self.curado == True and self.alive == True:
            #Curado
            fill(153, 51, 153)
            circle((self.position.x, self.position.y), self.size,mode=None)
            
    def apply_behaviour(self, boids):
        global  flag
        if self.alive == True:
            separation = self.separation(boids)
            alignment = self.align(boids)
            cohesion = self.cohesion(boids)

            self.acceleration += separation
            self.acceleration += alignment
            self.acceleration += cohesion
            self.colision(boids)
            #self.acceleration += colision


            #self.segregation(boids)
    def edges(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width
        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height


    def align(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vector = Vector(*np.zeros(2))
        for boid in boids:
            if boid.alive == True:
                if np.linalg.norm(boid.position - self.position) < self.perception:
                    avg_vector += boid.velocity
                    total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = (avg_vector / np.linalg.norm(avg_vector)) * self.max_speed
            steering = avg_vector - self.velocity
        return steering

    def cohesion(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        center_of_mass = Vector(*np.zeros(2))
        for boid in boids:
            if boid.alive == True:
                if np.linalg.norm(boid.position - self.position) < self.perception:
                    center_of_mass += boid.position
                    total += 1
        if total > 0:
            center_of_mass /= total
            vec_to_com = center_of_mass - self.position
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
            steering = vec_to_com - self.velocity
            if np.linalg.norm(steering)> self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force
        return steering

    def separation(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vector = Vector(*np.zeros(2))
        for boid in boids:
            if boid.alive == True:
                distance = np.linalg.norm(boid.position - self.position)
                if self.position != boid.position and distance < self.perception:
                    diff = self.position - boid.position
                    diff /= distance
                    avg_vector += diff
                    total += 1        
        if total > 0:
            avg_vector /= total
            if np.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
                
            steering = avg_vector 
            
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force
        return steering  
    
    def infection(self, boids):
        rng = default_rng()
        chance = rng.integers(low=0, high=1000)
        if self.infected == True:
            for boid in boids:
                if chance >= 700 and boid.curado == False and frames - self.days >240 and boid.usingmask == False:
                    if np.linalg.norm(boid.position - self.position) < self.perception:
                        boid.days = frames    
                        boid.infected = True
                if chance >= 900 and boid.curado == False and frames - self.days >240 and boid.usingmask == True or boid.curado == True:
                    if np.linalg.norm(boid.position - self.position) < self.perception:
                        boid.days = frames
                        boid.infected = True
                
    def livesordie(self):
        if self.infected == True:
            rng = default_rng()
            chance = rng.integers(low=0, high=1000)
            secondchance= rng.integers(low=0, high=1000)
            if  frames - self.days >720:
                if chance >= 966 and self.curado == False:
                    #morto
                        self.alive = False
                        self.infected = False
                elif secondchance >= 900: 
                    #Curado
                    print("Curado")
                    if self.infected == True and self.alive == True:
                        self.infected = False
                        self.curado = True

    def Usemask(self):
        rng =default_rng()
        chance = rng.integers(low=0, high=1000)
        secondchance= rng.integers(low=0, high=1000)
        if chance >= 900 and frames >=2000:
            self.usingmask = True
        if secondchance >= 900 and self.usingmask == True:
            self.usingmask = False
    
    def newaarrive(flock):
        rng =default_rng()
        chance = rng.integers(low=0, high=1000)
        secondchance= rng.integers(low=0, high=1000)
        if chance >= 990 and frames >=2000:
            flock.append(Boid(x = rng.integers(low=0, high=500),y = rng.integers(low=0, high=500),width=500, height=500,infected=True,curado=False,alive=True))
            print("Infectado")
        if secondchance >= 990 and frames >=1000:
            flock.append(Boid(x = rng.integers(low=0, high=500),y = rng.integers(low=0, high=500),width=500, height=500,infected=False,curado=False,alive=True))
            print("Saudavel")

    def byearrive(flock):
        rng =default_rng()
        chance = rng.integers(low=0, high=1000)
        if chance >= 990 and frames >=4000:
            del flock[-1]
            print("tchau")


    def colision(self, boids):
        steering = Vector(*np.zeros(2))
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.size and self != boid and boid.alive ==True:
                self.velocity = -self.velocity*self.max_speed -self.velocity
            #return steering

    def segregation(self,boids):
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.perception and boid.alive == True:
                self.velocity = self.velocity*self.max_speed
             
                
