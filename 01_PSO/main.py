# -*- coding: utf-8 -*-

import numpy as np
from math import pi, cos
import plotting as plt
import random


# Inputs
FUNCTION_NAME = "Rastrigin"
#FUNCTION_NAME = "Rosenbrock"  # UNTOGGLE TO CHANGE THE FUNCTION
N_PARTICLES = 5
PSO_ITERATIONS = 1000


# === Defining Benchmark Functions ===
def Rosenbrock(x, y):
    a = 0;
    b = 100;
    return (a-x)**2 + b*(y-x**2)**2;

def Rastrigin(x, y):
    return 10*2 + (x**2 - 10*cos(2*pi*x)) + (y**2 - 10*cos(2*pi*y))


# === define function ===
z_func = Rastrigin
if FUNCTION_NAME == "Rosenbrock":
    z_func = Rosenbrock

# === Calculating x,y Values ===
x, y = 0, 0
LIM_m_x, LIM_M_x = -1, 1
LIM_m_y, LIM_M_y = -1, 1

if FUNCTION_NAME == "Rosenbrock":
    LIM_m_x, LIM_M_x = -2, 2
    LIM_m_y, LIM_M_y = -1, 3
else: # Rastrigin
    LIM_m_x, LIM_M_x = -5, 5
    LIM_m_y, LIM_M_y = -5, 5

x = np.linspace(LIM_m_x, LIM_M_x, 200)
y = np.linspace(LIM_m_y, LIM_M_y, 200)


# === Initialization ===
def InitZfunction(n, x, y):
    start_part = []
    for i in range(n):
         start_part.append(np.array([random.choice(x), random.choice(y)]))
        
    return np.array(start_part)


# initialize particles
StartArray = InitZfunction(N_PARTICLES, x, y)


def InitVelocity():
    spam = []
    for i in range(N_PARTICLES):
        spam.append(np.array([random.randrange(-10,10,1), random.randrange(-10,10,1)])) #random velocity    #spam.append([0.0, 0.0])
    return np.array(spam)

def UpdateGb(t, z_func):
    current_best = z_func(gbest[0], gbest[1])
    for p in range(N_PARTICLES):
        new_best = z_func(CRON_S[t][p][0], CRON_S[t][p][1])
        if new_best < current_best:
            gbest[0] = CRON_S[t][p][0]
            gbest[1] = CRON_S[t][p][1]
            current_best = new_best

def InitPb(): #in time=0 everyone has the Pb in time=0
    spam = []
    for p in range(N_PARTICLES):
        spam.append(0)
    return np.array(spam)

def UpdatePb(t, z_func):
    spam = []
    for p in range(N_PARTICLES):
        last_Pb_t= CRON_Pb[t-1][p]
        last_Pb = z_func(CRON_S[last_Pb_t][p][0], CRON_S[last_Pb_t][p][1])
        new_Pb = z_func(CRON_S[t][p][0], CRON_S[t][p][1])
        if new_Pb < last_Pb:
            spam.append(t)
        else:
            spam.append(last_Pb_t)
    return np.array(spam)

def s(p, t):
    if t == 0:
        return CRON_S[0][p]
    next_pos = CRON_S[t-1][p] + CRON_V[t][p]
    
    # limiting movement in x-direction
    if next_pos[0]>LIM_M_x:
        next_pos[0]=LIM_M_x
    if next_pos[0]<LIM_m_x:
        next_pos[0]=LIM_m_x
    # limiting movement in y-direction 
    if next_pos[1]>LIM_M_y:
        next_pos[1]=LIM_M_y
    if next_pos[1]<LIM_m_y:
        next_pos[1]=LIM_m_y
            
    return next_pos #vp(t)

def v(p, t):
    a = 0.9-(0.5*(t/PSO_ITERATIONS)) # a= 0.9 -> 0.4
    b, c = 2, 2
    Rb, Rc = random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)  
    if t == 0:
        return CRON_V[0][p]
    #print("t->"+ str(t) + " i->"+ str(i))
    #print(str(len(CRON_Pb)))
    #print(CRON_Pb[t-1])
    last_Pb_t= CRON_Pb[t-1][p]
    Pb = CRON_S[last_Pb_t][p]
    #print(CRON_Gb[t-1])
    Gb = gbest
    #Gb = CRON_S[t-1][CRON_Gb[t-1]]
    
    return a*CRON_V[t-1][p] + b*Rb*(Pb - CRON_S[t-1][p]) + c*Rc*(Gb - CRON_S[t-1][p])


# === PSO iteration ===
CRON_S, CRON_V, CRON_Pb, gbest = [], [], [], []
CRON_S.append(StartArray)     # ARRAY OF [TIME][PARTICLE][Sxy]
CRON_V.append(InitVelocity()) # ARRAY OF [TIME][PARTICLE][Vxy]
CRON_Pb.append(InitPb())      # ARRAY OF [TIME][INDEX of PERSONAL BEST]

gbest = np.array([CRON_S[0][0][0], CRON_S[0][0][1]]) #just to initialize
UpdateGb(0, z_func) #tuple of Xgb-Ygb


# == Start the iterations ==
for t in range(1, PSO_ITERATIONS):

    cron_v_dataset = []
    for p in range(N_PARTICLES):
        cron_v_dataset.append(v(p, t))
    CRON_V.append(np.array(cron_v_dataset))
    
    #update position
    cron_s_dataset = []
    for p in range(N_PARTICLES):
        #print("t is: " + str(t))
        #print("len(CRON_S) is "+str(len(CRON_S)))
        cron_s_dataset.append(s(p, t))
    CRON_S.append(np.array(cron_s_dataset))

    # update Gb
    UpdateGb(t, z_func)

    #update Pb
    CRON_Pb.append(UpdatePb(t, z_func))


# == Plotting iterations ==
STEPPINGS = 200
print("PSO walkthroug (every ", STEPPINGS, " steps)")

colors = ['white', 'purple', 'orange', 'yellow', 'black']

round = 0
for t2 in range(PSO_ITERATIONS):

    STEPPINGS = 100
    if t2 % STEPPINGS != 0:
        continue
    
    v, ax = plt.Plot2D(x, y, z_func)
    array_old_X, array_old_Y = [], []
    
    for t in range(0, t2, STEPPINGS):
        if t == 0: #init
            for p in range(N_PARTICLES):
                #print(CRON_S[t][p][0], CRON_S[t][p][1])
                plt.DrawMarker2DEx(ax, CRON_S[t][p][0], CRON_S[t][p][1], colors[p], str(round))
                array_old_X.append(CRON_S[t][p][0])
                array_old_Y.append(CRON_S[t][p][1])
    
        else:#if t == PSO_ITERATIONS-1 or t%10==0:
            for p in range(N_PARTICLES):
                plt.PlottingSegment(ax, CRON_S[t][p][0], array_old_X[p], CRON_S[t][p][1], array_old_Y[p])
                array_old_X[p]=CRON_S[t][p][0]
                array_old_Y[p]=CRON_S[t][p][1]
                
                if t == PSO_ITERATIONS-1:
                    plt.DrawMarker2D(ax, CRON_S[t][p][0], CRON_S[t][p][1], True)
                else:
                    plt.DrawMarker2DEx(ax, CRON_S[t][p][0], CRON_S[t][p][1], colors[p], str(round))
    round +=1

    v.show()