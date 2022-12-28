import math as m
import numpy as np

class curvas:

    def __init__(self) -> None:
        pass
    #-------------------------------------------------------------------------------
    #  Bezier Control Points
    #-------------------------------------------------------------------------------
    def bezier_cps():

        i           = 0
        cpx_upper   = list()
        cpy_upper   = list()
        
        f = open('cp_upper.inp','r')
        for line in f:
            if( i > 0):
                cpx_upper.append(float(line.strip().split()[0]))
                cpy_upper.append(float(line.strip().split()[1]))                
            i += 1
        f.close()
        order_upper = i-2          # Polynomial_Order = Number of Points - 1 ( here I am discounting the first line.....)

        i           = 0
        cpx_lower   = list()
        cpy_lower   = list()

        f = open('cp_lower.inp','r')
        for line in f:
            if( i > 0):
                cpx_lower.append(float(line.strip().split()[0]))
                cpy_lower.append(float(line.strip().split()[1]))                
            i += 1
        f.close()
        order_lower = i-2          # Polynomial_Order = Number of Points - 1 ( here I am discounting the first line.....)

        return cpx_upper,cpy_upper,order_upper,cpx_lower,cpy_lower,order_lower

    def bezier_profiles(cpx,cpy,order):

    #  Some input data for the stretching function...
        nocp      = order + 1
        npts      = 58
        stre_coef = 95.0
        dx        = 1.0 / npts
        etau      = list()
        x         = list()

    #  Generating the profile bunching  - ATANH  distribution
    
        for i in range(npts+1):
            x.append(float(0.0 + i * dx))
            stre  = 1.0 + m.tanh(stre_coef*(x[i]-1.0)*m.pi/180.0) / m.tanh(stre_coef*m.pi/180.0)
            etau.append(float(stre+0.0))

    # Defining the coefficients of the PASCAL TRIANGLE.....
        lcni = list()
        for i in range(0, order+1, 1):
            aux = curvas.fat(order)/(curvas.fat(i)*curvas.fat(order-i))
            lcni.append(int(aux))
        duaux = [[0. for i in range(npts+1)] for k in range(order+1)]
        for i in range(0,npts+1,1):
            for k in range(0, order+1,1):
                duaux[int(k)][int(i)] = lcni[k]*(m.pow(etau[i],k))*(m.pow((1-etau[i]),(order-k)))

    #   Here I am putting the dul array into other arrays using the numpy lib.
        du            = np.matrix(duaux).T
        cpx2          = np.reshape(cpx, (nocp,1))
        cpy2          = np.reshape(cpy, (nocp,1))
        x_bezier      = du*cpx2
        y_bezier      = du*cpy2

    #
    #  Generationg the upper surface of the profile...it is symmetric
    #
        x1 = list()
        y1 = list()
        for i in range(0,npts+1):                                
            x1.append(float(x_bezier[i]))
            y1.append(float(y_bezier[i]))

        return x1,y1

    #-------------------------------------------------------------------------------
    #   Fatorial Function
    #-------------------------------------------------------------------------------
    def fat(n):
        if n == 0:
            return 1
        else:
            return n * curvas.fat(n-1)
