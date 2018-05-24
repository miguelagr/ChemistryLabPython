import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.integrate import simps
import scipy
#Parametros de las curvas
n=1
muA=-1.
muB=-2.
z = 6.
T = 6
kB = 1.
muAB=1
#numer de puntos
npo=1000
#numero de temperaturas
nT=100
#nT=5
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
temp=[]
curvas=[]
tans=[]
for i in range(nT):
    T= T - .035
    mu = gibbs(x1)
    #busca los minimos de la funcion
    minimo=scipy.optimize.fmin(gibbs,0.01,xtol=0.0001)
    tm=tan(x1,minimo)
    for i in x1:
        if abs(i-minimo) <= 0.001:
            iminimo=list(x1).index(i)
            break
    pp=encuentratan(x1,iminimo)
    itan.append(pp[0])
    rtan.append(pp[1])
    temp.append(T)
    tn = tan(x1,x1[pp[0]])
    curvas.append(mu)
    tans.append(tn)

for i in itan:
    print [i],gibbs(x1[i])


xitan=[x1[i] for i in itan]
xrtan=[x1[i] for i in rtan]
gitan=[gibbs(x1[i]) for i in itan]
grtan=[gibbs(x1[i]) for i in rtan]




LARGE_FONT= ("Verdana", 12)



class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Graficas")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):
    cont=None
    moles=None
    mmuA=None
    mmuB=None
    zz=None
    TT=None
    kkB=None
    mmuAB=None
    nnpo=None
    nnT=None
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.cont=controller
        label = tk.Label(self, text="Selecciona grafica", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
            
        button2 = ttk.Button(self, text="Energia libre de Gibbs",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Domo de estabilidad",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()
        button4 = ttk.Button(self, text="Calcular Graficas",
                            command=self.calcula)
        button4.pack()

        moles = ttk.Entry(self)
        self.moles=moles
        moles.pack()

        mmuA = ttk.Entry(self)
        self.mmuA=mmuA
        mmuA.pack()
 
        mmuB = ttk.Entry(self)
        self.mmuB=mmuB
        mmuB.pack()
 

        zz = ttk.Entry(self)
        self.zz=zz
        zz.pack()
 
        TT = ttk.Entry(self)
        self.TT=TT
        TT.pack()
 
        kkB = ttk.Entry(self)
        self.kkB=kkB
        kkB.pack()
 
        mmuAB = ttk.Entry(self)
        self.mmuAB=mmuAB
        mmuAB.pack()

        nnpo = ttk.Entry(self)
        self.nnpo=nnpo
        nnpo.pack()
         
        nnT = ttk.Entry(self)
        self.nnT=nnT
        nnT.pack()
 
 
    def calcula(self):
        global n
        global muA
        global muB
        global z
        global T
        global kB
        global muAB
        global npo
        global nT
        global x1
	n=float(self.moles.get())
	muA=-float(self.mmuA.get())
	muB=-float(self.mmuB.get())
	z = float(self.zz.get())
	T = float(self.TT.get())
	kB = float(self.kkB.get())
	muAB= float(self.mmuAB.get())
	#numer de puntos
	npo= int(self.nnpo.get())
	#numero de temperaturas
	#nT=100
	nT= int(self.nnT.get())
	#vector de abscisas
	x1=np.linspace(0.0001,0.999,npo)
        global itan
        global rtan
        global temp
        global curvas
        global tans
        itan=[]
        rtan=[]
        temp=[]
        curvas=[]
        tans=[]

	for i in range(nT):
	    T= T - .035
	    mu = gibbs(x1)
	    #busca los minimos de la funcion
	    minimo=scipy.optimize.fmin(gibbs,0.01,xtol=0.0001)
	    tm=tan(x1,minimo)
	    for i in x1:
	        if abs(i-minimo) <= 0.001:
	            iminimo=list(x1).index(i)
                    break
	    pp=encuentratan(x1,iminimo)
	    itan.append(pp[0])
	    rtan.append(pp[1])
	    temp.append(T)
	    tn = tan(x1,x1[pp[0]])
	    curvas.append(mu)
	    tans.append(tn)
	for i in itan:
	    print [i],gibbs(x1[i])
        global xitan
        global xrtan
	xitan=[x1[i] for i in itan]
	xrtan=[x1[i] for i in rtan]
	gitan=[gibbs(x1[i]) for i in itan] 
        grtan=[gibbs(x1[i]) for i in rtan]
        self.cont.show_frame(PageTwo)






#class PageOne(tk.Frame):

#    def __init__(self, parent, controller):
#        tk.Frame.__init__(self, parent)
#        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
#        label.pack(pady=10,padx=10)

#        button1 = ttk.Button(self, text="Back to Home",
#                            command=lambda: controller.show_frame(StartPage))
#        button1.pack()

#        button2 = ttk.Button(self, text="Page Two",
#                            command=lambda: controller.show_frame(PageTwo))
#        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Curvas", font=LARGE_FONT)
        label.pack(pady=10,padx=10)


        T=tk.Label(self,text="Cuadro de texto")
        T.pack(pady=10,padx=10)
 

        button1 = ttk.Button(self, text="Pagina principal",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(5,5), dpi=100)

        a = f.add_subplot(111)
        for i in curvas:
            a.plot(x1,i)
        for i in tans:
            a.plot(x1,i) 
        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Isotermas", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        T=tk.Label(self,text="Cuadro de texto\nLinea")
        T.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Pagina principal",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

 
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(xitan,temp,'.b',linewidth=1,markersize=12)
        a.plot(xrtan,temp,'.b',linewidth=1,markersize=12) 
        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        

app = SeaofBTCapp()
app.mainloop()

#Parametros de las curvas

