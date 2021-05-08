from p5 import *
import numpy as np
from boids import Boid
from data import Data
n=25;
width = 1000
height = 1000
flock=[]
infected=[]



for i in range(n):
    if i==0:
        flock.append(Boid(*np.random.rand(2)*1000, width, height,infected=True))
    else:
        flock.append(Boid(*np.random.rand(2)*1000, width, height,infected=False))

def setup():
    #this happens just once
    size(width, height) #instead of create_canvas


def draw():
    global flock

    background(30, 30, 47)

    for boid in flock:
        boid.edges()
        boid.apply_behaviour(flock)
        boid.update()
        boid.show()
        boid.infection(flock)
        boid.livesordie()
    Data.count(flock)
  

run()