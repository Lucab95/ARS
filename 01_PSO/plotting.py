# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:41:35 2020

@author: Adam, Daniel, Glauco
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def GetPlottingMatrices(x, y, func):
    X, Y = np.meshgrid(x, y)
    z = np.zeros(shape=(X.shape))    
    for ix in range(X.shape[0]):
        for iy in range(X.shape[0]):
            z[ix, iy] = func(X[ix, iy], Y[ix, iy])
    return X, Y, z
    
# =============================================================================

def Plot2D(x, y, func):
    X, Y, z = GetPlottingMatrices(x, y, func)
    
    # === Plotting: 2D - Heatmap ===
    fig = plt.figure()
    ax = fig.gca()
    
    plt.contourf(X, Y, z, cmap=cm.jet)
    plt.colorbar(aspect=5)
    plt.xlabel('x')
    plt.ylabel('y')
    
    return plt, ax

def Plot2DDirect(x, y, func):
    plt, ax = Plot2D(x, y, func)
    plt.show()

def Plot3D(x, y, func):
    X, Y, z = GetPlottingMatrices(x, y, func)
    
    # === Plotting: 3D ===
    fig = plt.figure()
    ax = Axes3D(fig)
    surf = ax.plot_surface(X, Y, z, cmap=cm.jet, linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.75, aspect=5)
    plt.xlabel('x')
    plt.ylabel('y')
    
    return plt, ax

def Plot3DDirect(x, y, func):
    plt, ax = Plot3D(x, y, func)
    plt.show()
    
# =============================================================================
    
def DrawMarker2D(ax, x, y, final_mark):
    if final_mark==True:
        ax.plot(x, y, color='red', marker='x', markersize=20, markeredgewidth=4)
    else:
        ax.plot(x, y, color='magenta', marker='o', markersize=5, markeredgewidth=4)
        
def DrawMarker2DEx(ax, x, y, col, value):
    ax.plot(x, y, color=col, marker='o', markersize=5, markeredgewidth=4)
    ax.annotate(value, (x, y))
    
def DrawMarker3D(ax, x, y):
    ax.plot([x], [y], color='red', marker='x', markersize=20, markeredgewidth=4)
    
def PlottingSegment(ax, Xa, Xb, Ya, Yb): # segment from points A to B
    ax.plot([Xa, Xb], [Ya, Yb], linewidth=1, color='black')