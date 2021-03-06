from p5 import *
import numpy as np
from numpy.random import default_rng
from boids import Boid
from data import Data
n=30;
width = 1920
height = 1080
flock=[]
infected=[]
rng = default_rng()
frames=0

for i in range(n):
    x = rng.integers(low=0, high=1920)
    y = rng.integers(low=0, high=1080)

    if i==0:
        flock.append(Boid(x,y, width, height,infected=True,curado=False,alive=True))
    else:
        flock.append(Boid(x,y, width, height,infected=False,curado=False,alive=True))

def setup():
    #this happens just once
    size(width, height) #instead of create_canvas


def draw():
    global flock,frames
  
    background(30, 30, 47)


    for boid in flock:
        boid.edges()
        boid.apply_behaviour(flock)
        boid.infection(flock)
        boid.update() 
        boid.show()
        boid.livesordie()
    Data.count(flock)
  

run()