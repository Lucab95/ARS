import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# == Plotting iterations ==
def GetPlottingMatrices(x, y, func):
    X, Y = np.meshgrid(x, y)
    z = np.zeros(shape=(X.shape))
    for ix in range(X.shape[0]):
        for iy in range(X.shape[0]):
            z[ix, iy] = func(X[ix, iy], Y[ix, iy])
    return X, Y, z

def PlotFunction(x, y, func):
    X, Y, z = GetPlottingMatrices(x, y, func)
    fig = plt.figure()
    ax = fig.gca()
    plt.contourf(X, Y, z, cmap=cm.jet)
    plt.colorbar(aspect=5)
    plt.xlabel('x')
    plt.ylabel('y')
    return plt, ax

def DrawMarker(ax, x, y, value, is_final_mark):
    if is_final_mark == True:
        ax.plot(x, y, color='red', marker='x', markersize=20, markeredgewidth=4)
    else:
        ax.plot(x, y, color='magenta', marker='o', markersize=5, markeredgewidth=4)
    ax.annotate(value, (x, y))

def PlottingSegment(ax, Xa, Xb, Ya, Yb):  # segment from points A to B
    ax.plot([Xa, Xb], [Ya, Yb], linewidth=1, color='black')


# errors.append([np.square(np.subtract(x, output)).mean(), i])
# errors = np.array(errors)
# plt.plot(errors[:, 1], errors[:, 0])
# plt.xlabel('Mean square error')
# plt.ylabel('Number epochs')
# plt.show()