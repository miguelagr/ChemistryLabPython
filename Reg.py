#!/usr/bin/python
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from scipy.integrate import simps
import scipy
import Tkinter as tk
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Parametros de las curvas
n=1
muA=-1.
muB=-2.
z = 6.
T = 6.
kB = 1.
muAB=1
#numer de puntos
npo=1000
#numero de temperaturas
nT=5
#nT=1
#vector de abscisas
x1=np.linspace(0.0001,0.999,npo)

#Funcion de Gibbs
def gibbs(x):
    return x*muA + (1.-x)*muB +n*kB*T*(x*np.log(x)+(1.-x)*np.log(1.-x))+12*x*(1-x)

#Derivada de la funcion
def dgibbs(x):
    return muA-muB+n*kB*T*(np.log(x)-np.log(1.-x))-12.*2*x+12

#Definicion de tangente a la curva dada la derivada
def tan(x,p):
    #print dgibbs(p)
    return dgibbs(p)*x+gibbs(p)-dgibbs(p)*p


def onpick(event):
    thisline=event.artist
    xdata=thisline.get_xdata()
    ydata=thisline.get_ydata()
    print xdata[event.ind]

#Encuentra la tangente a dos puntos de manera iterativa
#a partir de un punto base
def encuentratan(x,p):
    encontrado=0
    for i in range(p,npo):
        t=tan(x,x[i])
        for j in range(0,npo):
            if t[j] > gibbs(x[j]):
                return (i,j)


#obtener una familia de curvas

itan=[]
rtan=[]
plt.figure()
for i in range(nT):
    T= T - .35
    mu = gibbs(x1)
    minimo=scipy.optimize.fmin(gibbs,0.01,xtol=0.0001)
    tm=tan(x1,minimo)
    for i in x1:
        if abs(i-minimo) <= 0.001:
            iminimo=list(x1).index(i)
            #print x1[list(x1).index(i)]
            break
    pp=encuentratan(x1,iminimo)
    itan.append(pp[0])
    rtan.append(pp[1])
    tn = tan(x1,x1[pp[0]])
#    tn1 = tan(x1,x1[encuentratan(x1,iminimo)[1]-1])
#    tn2 = tan(x1,x1[encuentratan(x1,iminimo)[0]])
#    tn3 = tan(x1,x1[encuentratan(x1,iminimo)[0]-1])
#    plt.plot(minimo,gibbs(minimo),'o')
#    plt.plot(x1,tn)
#    plt.plot(x1,tn1)
    #plt.plot(x1,tm)
    plt.plot(x1,mu)
#    plt.plot(x1,tn3)
    plt.plot(x1,tn)
#plt.show()

plt.figure()

for i in itan:
    print [i],gibbs(x1[i])

gitan=[gibbs(x1[i]) for i in itan]
grtan=[gibbs(x1[i]) for i in rtan]
plt.plot(itan,gitan,'.b-',linewidth=1,markersize=12)
plt.plot(rtan,grtan,'.b-',linewidth=1,markersize=12)
plt.show()
 
#plt.ion()
#f.canvas.mpl_connect('pick_event',onpick)  
#plt.plot(0.4,-2.01,'o',picker=5)
#plt.ion()
#canvas=FigureCanvasTkAgg(f,master=ventana)
#plot_w=canvas.get_tk_widget()
#f.canvas.draw()
#plt.ylim((0,5))
#ventana.mainloop()

#ventana = tk.Tk()
#ventana.title("Algo")
#marco=tk.Frame(ventana)



