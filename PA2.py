#If using Jupyter note book, you may want to add the following magic at the beginning of your Codes
# %matplotlib tk
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import math

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.view_init(azim=30)
ax.set_xlim3d(0,5)
ax.set_ylim3d(0,5)
ax.set_zlim3d(0,5)
ax.set_aspect("equal")


def init():
    i=0
    fbo=np.array([1, 1, 1])
    fbx=fbo+np.array([1, 0, 0])
    fby=fbo+np.array([0, 1, 0])
    fbz=fbo+np.array([0, 0, 1])
    xb = Arrow3D([fbo[0],fbx[0]],[fbo[1],fbx[1]],[fbo[2],fbx[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="k")
    yb = Arrow3D([fbo[0],fby[0]],[fbo[1],fby[1]],[fbo[2],fby[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="b")
    zb = Arrow3D([fbo[0],fbz[0]],[fbo[1],fbz[1]],[fbo[2],fbz[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="r")
    ax.add_artist(xb)
    ax.add_artist(yb)
    ax.add_artist(zb)
    return xb, yb, zb

def animate(i):
    fbo=np.array([1+i/10, 1+i/10, 1+i/10])
    fbx=fbo+np.array([1, 0, 0])
    fby=fbo+np.array([0, 1, 0])
    fbz=fbo+np.array([0, 0, 1])
    xb = Arrow3D([fbo[0],fbx[0]],[fbo[1],fbx[1]],[fbo[2],fbx[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="k")
    yb = Arrow3D([fbo[0],fby[0]],[fbo[1],fby[1]],[fbo[2],fby[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="b")
    zb = Arrow3D([fbo[0],fbz[0]],[fbo[1],fbz[1]],[fbo[2],fbz[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="r")
    ax.add_artist(xb)
    ax.add_artist(yb)
    ax.add_artist(zb)
    return xb, yb, zb

I = np.matrix('1,0,0; 0,1,0 ; 0,0,1')

def expConfig(S, T0):
    #S is the screw axis (w,v),
    #T0 is the initial frame configuration
    #By theorem 1, we can find e^[S]theta:
    w = np.matrix(S[0:3])
    v = np.matrix(S[3:6])
    ret = []
    #if w == 0
    if np.count_nonzero(w) == 0:
        ret = np.concatenate((I, [[0],[0],[0]]), axis=1) #Theta is 0
        ret = np.concatenate((ret, [[0,0,0,1]]), axis=0)
        return ret;
    #if w != 0
    else:
        #e^[w]theta
        theta = np.linalg.norm(w)
        wHat = w/theta
        wSq = np.matrix([[0, -w[0,2], w[0,1]],
                         [w[0,2], 0, -w[0,0]],
                         [-w[0,1], w[0,0], 0]])

        ewt = I + wSq*math.sin(theta) + wSq*wSq*(1-math.cos(theta))

        print(ewt)

        print("It isn't empty")


S = [0,0,1,4,5,6]
T = []
expConfig(S,T)


#ani = animation.FuncAnimation(fig, animate, np.arange(1, 50), interval=25, blit=True, init_func=init)

#plt.show()


