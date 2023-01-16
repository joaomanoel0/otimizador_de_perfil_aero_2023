# Classe de Desempenho do MDO 2023

import math as m
import matplotlib.pyplot as plt
from classe_curvas import curvas

class desempenho:

    def __init__(self, g, mu, K, Clmax, Cdmin, hw, bw, Sw, AD, prop):
        self.g = g
        self.mu = mu
        self.K = K
        self.Clmax = Clmax
        self.Cdmin = Cdmin
        self.hw = hw
        self.bw = bw
        self.Sw = Sw
        self.AD = AD
        self.prop = prop
        self.Mtow = desempenho.mtow(self, AD)
        self.W = self.Mtow*self.g
        pass

    def razao_subida(AD, V): # Definição da função que denota a razão de subida para a hélice escolhida (14x7-E)
        if AD == 'F':
            return -4.73 + 0.679*V - 0.0186*V**2
        elif AD == 'S':
            return -5.12 + 0.663*V - 0.0177*V**2
        elif AD == 'I':
            return -5.27 + 0.639*V - 0.0169*V**2

    def vel_estol(self, rho): # Velocidade na qual a aeronave entra em 'stall'
        return m.sqrt((2*(self.W))/(rho*self.Sw*self.Clmax))
    '''
    #  As velocidades de Ground Roll, Rotation e Transition somente serão aproximadas para decolagens com obstáculos (GUDMUNDSSON, 2013)

    def vel_ground_roll(self, rho):
        return 1.1*desempenho.vel_estol(self, rho)

    def vel_rotação(self, rho):
        return 1.1*desempenho.vel_estol(self, rho)
    
    def vel_transição(self, rho):
        return 1.15*desempenho.vel_estol(self, rho)
    '''
    def vel_liftoff(self, rho): # Velocidade estimada para decolagem "Vlof" (ANDERSON, 2015)
        return 1.2*desempenho.vel_estol(self, rho)

    def vel_liftoff_070(self, rho): # Velocidade ideal estimada para a subida "Vlof/raiz(2)"
        return (desempenho.vel_liftoff(self, rho))/m.sqrt(2)

    def vel_aprroch(self, rho): # Velocidade com que a aeronave se aproxima da pista de pouso (FAR Part-23)
        return 1.3*desempenho.vel_estol(self, rho)

    def vel_landing(self, rho): # Velocidade ideal estimada durante o pouso "Vappr/raiz(2)"
        return (desempenho.vel_aprroch(self, rho)/m.sqrt(2))

    def vel_max_alcance(self, rho): # Velocidade de máximo alcance, tração mínima requerida ou de máxima eficiência aerodinâmica
        return ((2*(self.W)/(rho*self.Sw))**0.5)*(((self.K)/self.Cdmin)**0.25)

    def vel_max_autonomia(self, rho): # Velocidade de máxima autonomia ou de potência requerida mínima 
        return ((2*(self.W)/(rho*self.Sw))**0.5)*(((self.K)/(3*self.Cdmin))**0.25)

    def Cl_ideal(self):
        efeito_solo = ((16*self.hw/self.bw)**2)/((1+(16*self.hw/self.bw)**2)) # Efeito solo durante a decolagem e o pouso
        return self.mu/(2*efeito_solo*self.K)

    def Cd_ideal(self):
        efeito_solo = ((16*self.hw/self.bw)**2)/((1+(16*self.hw/self.bw)**2)) # Efeito solo durante a decolagem e o pouso
        return self.Cdmin + efeito_solo*self.K*(desempenho.Cl_ideal(self)**2)

    def ponto_projeto(self):
        Cl_asterix = m.sqrt(self.Cdmin/self.K) # Coef. de sustentação que maximiza a eficiência aerodinâmica - ou o alcance, (Cl*)
        #Cl_asterix =  m.sqrt((3*self.Cdmin)/self.K) # Coef. de sustentação que permite planeio com máxima autonomia (Cl*)
        #Cd_asterix = self.Cdmin + self.K*Cl_asterix**2 # Coef. de arrasto para o ponto de projeto [Equivale ao "(2*self.Cdmin)"]
        E_max = Cl_asterix/(2*self.Cdmin) # Eficiência aerodinâmica máxima também escrito como (L/D)max
        return E_max

    def decolagem(self, rho, AD):
        T_Vlof_r2 = curvas.tracao(AD, desempenho.vel_liftoff_070(self, rho), self.prop) # Tração estimada na velocidade da norma aeronáutica
        D_Vlof_r2 = 0.5*rho*((desempenho.vel_liftoff_070(self, rho))**2)*self.Sw*desempenho.Cd_ideal(self)
        L_Vlof_r2 = 0.5*rho*((desempenho.vel_liftoff_070(self, rho))**2)*self.Sw*desempenho.Cl_ideal(self)
        ac_media = (1/self.Mtow)*(T_Vlof_r2-D_Vlof_r2-self.mu*((self.W)-L_Vlof_r2))
        Sg = (1.44*(self.W)**2)/(self.g*rho*self.Sw*self.Clmax*(T_Vlof_r2-D_Vlof_r2-self.mu*((self.W)-L_Vlof_r2)))
        t_Sg = m.sqrt(2*Sg/ac_media)
        return ac_media, Sg, t_Sg

    def subida(self, AD, V):
        v = 0
        rate_climb = [] # Cria uma lista que irá conter a razão de subida em cada velocidade de V = 0 até V = 30 m/s
        while v <= 30:
            rate_climb.append(desempenho.razao_subida(AD, v)) # Guarda os valores de R/C em rate_climb
            v += 0.001 # Diferencial que funciona como contador
        max_rate_c = max(rate_climb) # Pega a maior razão de subida (R/C_max) em m/s
        vel_h = (rate_climb.index(max_rate_c)+1)*0.001 # Pega a velocidade da aeronave durante o R/C_max
        max_ang_subida = m.asin(max_rate_c/vel_h)*(180/m.pi) # Calcula o ângulo de subida para o R/C_max em graus
        ang_subida = m.asin(desempenho.razao_subida(AD, V)/V)*(180/m.pi) # Calcula o ângulo de subida para um dado 'V' em graus
        return max_rate_c, vel_h, max_ang_subida, ang_subida

    #def cruzeiro():

    def pouso(self, rho):
        D_Vland = 0.5*rho*((desempenho.vel_landing(self, rho))**2)*self.Sw*desempenho.Cd_ideal(self)
        L_Vland = 0.5*rho*((desempenho.vel_landing(self, rho))**2)*self.Sw*desempenho.Cl_ideal(self)
        Sland_FAR = (1.69*(self.W)**2)/(self.g*rho*self.Sw*self.Clmax*(D_Vland+self.mu*((self.W)-L_Vland)))
        D_Vstall = 0.5*rho*((desempenho.vel_estol(self, rho)/m.sqrt(2))**2)*self.Sw*desempenho.Cd_ideal(self)
        L_Vstall = 0.5*rho*((desempenho.vel_estol(self, rho)/m.sqrt(2))**2)*self.Sw*desempenho.Cl_ideal(self)
        Sland_real = ((self.W)**2)/(self.g*rho*self.Sw*self.Clmax*(D_Vstall+self.mu*((self.W)-L_Vstall)))
        ang_planeio = m.atan(1/desempenho.ponto_projeto(self))*(180/m.pi) # Calcula o ângulo de planeio para (L/D)max em graus
        vel_planeio = m.sqrt((2*self.W*m.cos(ang_planeio*m.pi/180))/(rho*self.Sw*desempenho.Cl_ideal(self)))
        return Sland_FAR, Sland_real, ang_planeio, vel_planeio

    #def envelope_de_voo():

    def mtow(self, AD):
        rho = 1
        Carga_util = []  #[[Sg1_F,W1_F],[Sg2_F],[Sg3_F,W3_F],...[Sgi_F,Wi_F],[Sg1_S,W1_S]...[Sgi_S,Wi_S],[Sg1_I,W1_I],...[Sgi_I,Wi_I]]
        while rho <= 3:
            mtow = 12.0 # MTOW inicial
            if rho == 1: rho = 1.225; ad = 'F' # Troca o valor de rho=1 para rho=1.225 kg/m³ e atribui o valor correspondente (ad) à curva de tração
            elif rho == 2: rho = 1.156; ad = 'S' # Troca o valor de rho=2 para rho=1.156 kg/m³ e atribui o valor correspondente (ad) à curva de tração
            else: rho = 1.090; ad = 'I' # Troca o valor de rho=3 para rho=1.090 kg/m³ e atribui o valor correspondente (ad) à curva de tração
            while mtow <= 20:
                W = mtow*self.g
                T_Vlof_r2 = curvas.tracao(ad, (1.2*(m.sqrt((2*W)/(rho*self.Sw*self.Clmax))))/m.sqrt(2), self.prop) # ad, 'Vlof/sqrt(2)' e Hélice
                D_Vlof_r2 = 0.5*rho*(((1.2*(m.sqrt((2*W)/(rho*self.Sw*self.Clmax))))/m.sqrt(2))**2)*self.Sw*desempenho.Cd_ideal(self)
                L_Vlof_r2 = 0.5*rho*(((1.2*(m.sqrt((2*W)/(rho*self.Sw*self.Clmax))))/m.sqrt(2))**2)*self.Sw*desempenho.Cl_ideal(self)
                Sg = (1.44*W**2)/(self.g*rho*self.Sw*self.Clmax*(T_Vlof_r2-D_Vlof_r2-self.mu*(W-L_Vlof_r2)))
                if Sg <= 100:
                    Carga_util.append([Sg, W, rho])
                else:
                    break
                mtow += 0.1
                #print("zero") # Usado para testar se não estaria preso em loop infinito (Não descomentar!)
            if rho == 1.225: rho = 2
            elif rho == 1.156: rho = 3
            else: break
        x1, x2, x3 = [],[],[] # Valores de distância de decolagem para diferentes pesos na densidade do ar de 0m, 600m e 1200m
        y1, y2, y3 = [],[],[] # Valores de Pesos (W) diferentes para deolagem na densidade do ar de 0m, 600m e 1200m
        #print(Carga_util) # Verifica os valores de SG e W para cada rho
        for i in Carga_util:
            if i[2] == 1.225:
                x1.append(i[0]) # Valores de dist. de decolagem com rho = 1.225 kg/m³
                y1.append(i[1]) # Valores de Peso com rho = 1.225 kg/m³
                if i[0] <= 58: # Distância (m) que se espera que a aeroanave atinja a velocidade de decolagem em rho = 1.225 kg/m³ 
                    mtowF = i[1]/self.g # Se o menor elemento de i[0] > "condição acima", então mtowI = 0 e a linha 83 resulta em div/0
            elif i[2] == 1.156:
                x2.append(i[0]) # Valores de dist. de decolagem com rho = 1.156 kg/m³
                y2.append(i[1]) # Valores de Peso com rho = 1.156 kg/m³
                if i[0] <= 58: # Distância (m) que se espera que a aeroanave atinja a velocidade de decolagem em rho = 1.156 kg/m³
                    mtowS = i[1]/self.g # Se o menor elemento de i[0] > "condição acima", então mtowI = 0 e a linha 83 resulta em div/0
            elif i[2] == 1.090:
                x3.append(i[0]) # Valores de dist. de decolagem com rho = 1.090 kg/m³
                y3.append(i[1]) # Valores de Peso com rho = 1.090 kg/m³
                if i[0] <= 58: # Distância (m) que se espera que a aeroanave atinja a velocidade de decolagem em rho = 1.090 kg/m³
                    mtowI = i[1]/self.g # Se o menor elemento de i[0] > "condição acima", então mtowI = 0 e a linha 83 resulta em div/0
            else:
                break
        plt.plot(x1, y1, ls='solid', lw='1', color='g', label='SG para rho = 1.225 kg/m³')
        plt.plot(x2, y2, ls='solid', lw='1', color='k', label='SG para rho = 1.156 kg/m³')
        plt.plot(x3, y3, ls='solid', lw='1', color='r', label='SG para rho = 1.090 kg/m³')
        plt.title('Influência do peso (W) na distância de decolagem (SG)')
        plt.xlabel('Distância de decolagem (m)', fontsize=10)
        plt.ylabel('Peso (N)', fontsize=10)
        plt.legend()
        plt.axis("auto")
        plt.show()
        if AD == 'F':
            print(f'\nO mtow encontrado máximo é: {mtowF} kg') # Verifica o mtow usado para rho = 1.225kg/m³
            return mtowF
        elif AD == 'S':
            print(f'\nO mtow encontrado máximo é: {mtowS} kg') # Verifica o mtow usado para rho = 1.156kg/m³
            return mtowS
        elif AD == 'I':
            print(f'\nO mtow máximo encontrado é: {mtowI} kg') # Verifica o mtow usado para rho = 1.090kg/m³
            return mtowI
