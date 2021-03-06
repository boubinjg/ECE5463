#If using Jupyter note book, you may want to add the following magic at the beginning of your Codes
# %matplotlib tk
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import math

Tnew = np.matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

def init():
    i=0
    fbo=np.array([1, 1, 1])
    fbx=fbo+np.array([1, 0, 0])
    fby=fbo+np.array([0, 1, 0])
    fbz=fbo+np.array([0, 0, 1])
    fpb = np.array([1,2,3])
    fs = [1,0,0]

    xb = Arrow3D([fbo[0],fbx[0]],[fbo[1],fbx[1]],[fbo[2],fbx[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="k")
    yb = Arrow3D([fbo[0],fby[0]],[fbo[1],fby[1]],[fbo[2],fby[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="b")
    zb = Arrow3D([fbo[0],fbz[0]],[fbo[1],fbz[1]],[fbo[2],fbz[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="r")
    pb = Arrow3D([fbo[0],fbz[0]],[fbo[1],fbz[1]],[fbo[2],fbz[2]], mutation_scale=15, lw=2, arrowstyle="-|>",color="r")
    ps = Arrow3D([1,fs[0]],[1,fs[1]],[1,fs[2]], mutation_scale=15, lw=2, arrowstyle="-|>",color="r")


    ax.add_artist(xb)
    ax.add_artist(yb)
    ax.add_artist(zb)
    ax.add_artist(pb)
    ax.add_artist(ps)
    return xb, yb, zb, pb, ps

def animate(i):
    #fbo=np.array([1+i/10, 1+i/10, 1+i/10])
    Tnew = screwMotion(s,h,q,theta+(i/25),T0)
    fpb = np.transpose(Tnew)*[[1],[2],[3],[1]]

    fbo=np.array([Tnew[0,3],Tnew[1,3],Tnew[2,3]])
    fbx=fbo+np.array([Tnew[0,0], Tnew[0,1], Tnew[0,2]])
    fby=fbo+np.array([Tnew[1,0], Tnew[1,1], Tnew[1,2]])
    fbz=fbo+np.array([Tnew[2,0], Tnew[2,1], Tnew[2,2]])
    xb = Arrow3D([fbo[0],fbx[0]],[fbo[1],fbx[1]],[fbo[2],fbx[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="k")
    yb = Arrow3D([fbo[0],fby[0]],[fbo[1],fby[1]],[fbo[2],fby[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="b")
    zb = Arrow3D([fbo[0],fbz[0]],[fbo[1],fbz[1]],[fbo[2],fbz[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="r")
    pb = Arrow3D([fbo[0],fpb[0]],[fbo[1],fpb[1]],[fbo[2],fpb[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="g")
    ps = Arrow3D([0,2*s[0]],[0,2*s[1]],[0,2*s[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color="m")

    ax.add_artist(xb)
    ax.add_artist(yb)
    ax.add_artist(zb)
    ax.add_artist(pb)
    ax.add_artist(ps)
    return xb, yb, zb, pb, ps

I = np.matrix('1,0,0; 0,1,0 ; 0,0,1')

def expConfig(S, theta, T0):
    #S is the screw axis (w,v) (assumes ||w|| == 1)
    #T0 is the initial frame configuration
    #By theorem 1, we can find e^[S]theta:
    print("Calculating e^[s]theta")
    w = np.matrix(S[0:3])
    v = np.matrix(S[3:6])
    ret = []
    #if w == 0
    if np.count_nonzero(w) == 0:
        print("w == 0")
        vt = v*theta
        evt = np.concatenate((I, np.transpose(vt)), axis=1)
        evt = np.concatenate((evt, [[0,0,0,1]]), axis=0)
        print("e^[V]theta: ")
        print(evt)
        Tnew = evt*T0
        return Tnew
    #if w != 0
    else:
        print("w != 0")
        #e^[w]theta
        #[wHat]
        wSq = np.matrix([[0, -w[0,2], w[0,1]],
                         [w[0,2], 0, -w[0,0]],
                         [-w[0,1], w[0,0], 0]])
        #e^[w]*theta
        ewt = I + wSq*math.sin(theta) + wSq*wSq*(1-math.cos(theta))
        print("e^[w]theta: ")
        print(ewt)
        #G(Theta)*v
        gtv = I*theta + (1-math.cos(theta))*wSq + (theta - math.sin(theta))*wSq*wSq;
        gtv = gtv*np.transpose(v); #v is a row vector
        print("G(theta)*v")
        print(gtv)
        #e^[V]theta
        evt = np.concatenate((ewt, gtv), axis=1)
        evt = np.concatenate((evt, [[0,0,0,1]]), axis=0)
        print("e^[V]theta")
        print(evt)
        #multiply e^[V]Theta * T0
        Tnew = evt * T0;

        return Tnew

def screwMotion(s,h,q,theta,T0):
    #convert s,h,q to a format for the previous func
    w = s
    v = np.multiply(-1, (np.cross(w,q))) + np.multiply(h, w)

    S = (np.concatenate((w, v), axis=0))
    print(S)
    Tnew = expConfig(S, theta, T0)
    print("TNEW ============")
    print(Tnew)
    return Tnew

#S = [0,0,0,1,0,0]
theta = 1
T0 = np.matrix([[0,1,0,0],
                [0,0,1,0],
                [1,0,0,0],
                [0,0,0,1]])

s = [1,0,0]
q = [0,0,1]

h = 1
theta = .5
screwMotion(s,h,q,theta,T0)


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.view_init(azim=30)
ax.set_xlim3d(-3,3)
ax.set_ylim3d(-3,3)
ax.set_zlim3d(-3,3)
ax.set_aspect("equal")

ani = animation.FuncAnimation(fig, animate, np.arange(0, 100), interval=25, blit=True, init_func=init)

plt.show()
