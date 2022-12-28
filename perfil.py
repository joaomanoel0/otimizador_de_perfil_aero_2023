from xfoilwithpython.classe_Bezier import curvas
from xfoilwithpython.classe_Xfoil import xfoil
from matplotlib import pyplot
import subprocess
import numpy as np

class perfil_info:
    def __init__(self, x_upper, y_upper, x_lower, y_lower):
        self.x_upper = x_upper
        self.y_upper = y_upper
        self.x_lower = x_lower
        self.y_lower = y_lower
        self.order_u = len(x_upper)-1
        self.order_l = len(x_lower)-1
    
    def monta_perfil(self):
        xu,yu = curvas.bezier_profiles(self.x_upper,self.y_upper,self.order_u)
        f1 = open('profile.dat','w') 
        x = list()
        y = list()
        for i in reversed(range(0,len(xu))):                     #  Writting the upper surface...
            f1.write('%9.6f %9.6f\n' % (xu[i],yu[i]))
            x.append(float(xu[i]))
            y.append(float(yu[i]))
        # Generating the lower Side of the profile    
        xl,yl = curvas.bezier_profiles(self.x_lower,self.y_lower,self.order_l)          
        for i in range(0,len(xl)):                               #  Writting the lower airfoil...
            f1.write('%9.6f %9.6f\n' % (xl[i],yl[i]))
            x.append(float(xl[i]))
            y.append(float(yl[i]))
        f1.close()  
        size = 5.0
        pyplot.figure(figsize=(2*size,size))
        pyplot.xlabel('x', fontsize=16)
        pyplot.ylabel('y', fontsize=16)
        pyplot.xlim(-0.20, 1.2)
        pyplot.ylim(-0.18, 0.18)
        pyplot.plot(x,y)        
        pyplot.plot(self.x_upper,self.y_upper,'--ro')
        pyplot.plot(self.x_lower,self.y_lower,'--ro')    
        #pyplot.show()
        pyplot.savefig('perfil_gerado.png', format = 'png')

    
    def getparametros_perfil(self):
        xfoil_1 = xfoil("profile", 0, 0, 0, 433823, 0.04, 7)
        xfoil_1.input_xfoil() #objeto de análise

        '''Objeto modelo: 
        xfoil_0 = xfoil("s1223rtl", 0 , 15, 1, 1000000, 0.04, 50)
        xfoil_0.input_xfoil()'''

        #Input do objeto(perfil) para análise no Xfoil

        subprocess.call("xfoil.exe < input_file.in", shell=True)
        print("\n ok \n")
        polar_data = np.loadtxt("polar_file.txt", skiprows=12)
        print("\n ok2 \n")
        # Lendo os valores de CL e CD do arquivo polar_file.txt

        with open("polar_file.txt", "r") as arq:
            lista = arq.readlines() #readlines transforma o arquivo lido em uma lista (algo mais facil de tratar em python)
        #print(lista)

        for line in lista:
            if "0.000" in line:
                #print(line[10:17])
                if line[10] == "-":
                    CL = float(line[10:17])
                    print(CL, end=" ")
                else:
                    CL = float(line[11:17])
                    print(CL, end=" ")
                CD = float(line[20:27])
                print(CD)

        print(f'Valor do CL = {CL}, valor do CD = {CD}')
        return CL, CD