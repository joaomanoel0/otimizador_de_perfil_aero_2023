import matplotlib.pyplot as plt
from perfil import Perfil
import itertools
import numpy as np
import random
from operator import itemgetter, attrgetter

class otimizador:

    def __init__(self, retorno) -> None:
        self.retorno = retorno
        #self.new_method()

    # método que gera pontos no palno x e y para serem utilizados na construção de um perfil com o método de Bezier
    # sendo que upper é para definir se os pontos serão nos quadrantes superiores ou inferiores do plano cartesiano
    def gera_pontos(upper = True, sigma = 0.01):
        proximo = False
        if upper == True: quantidade_pontos = 9
        else: quantidade_pontos = 10

        vetx = list(itertools.repeat(0., quantidade_pontos))
        vety = list(itertools.repeat(0., quantidade_pontos))

        for i in range(quantidade_pontos):
            if i == quantidade_pontos-1:
                vetx[quantidade_pontos-1], vety[quantidade_pontos-1] = 1., 0.
            elif i == quantidade_pontos-2:
                if upper == False:
                    vetx[i] = random.gauss(0.85, sigma)
                    vety[i] = (random.uniform(0.10, -0.05))
                else:
                    vetx[i] = random.gauss(0.95, sigma)
                    vety[i] = (random.uniform(0.0, 0.10))
                
            elif i == quantidade_pontos-3 and upper == True:
                vetx[i] = random.gauss(0.90, sigma)
                vety[i] = (random.uniform(0.01, 0.10))
            elif i == 1: 
                if upper == False:
                    vety[i] = random.uniform(-0.01, -0.06)
                else:
                    vety[i] = random.uniform(0.02, 0.08)
            elif i == 2:
                if upper == False:
                    vetx[i] = random.gauss(0.05, sigma)
                    vety[i] = (random.uniform(0.0, -0.06))
                else:
                    vetx[i] = random.gauss(0.15, sigma)
                    vety[i] = (random.uniform(0.15, 0.23))
            elif i == 3:
                if upper == False:
                    vetx[i] = random.gauss(0.10, sigma)
                    vety[i] = (random.uniform(0.0, -0.06))
                else:
                    vetx[i] = random.gauss(0.30, sigma)
                    vety[i] = (random.uniform(0.15, 0.23))
            elif i != 0:
                if upper == True:
                    vety[i] = random.uniform(0.15, 0.23)
                    if proximo == False:
                        vetx[i], proximo = random.gauss(0.50, sigma), 1
                    elif proximo == 1:
                        vetx[i] = random.gauss(0.75, sigma)
                else:
                    vety[i] = random.uniform(0.15, -0.06)
                    if proximo == False:
                        vetx[i], proximo = random.gauss(0.20, sigma), 1
                    elif proximo == 1:
                        vetx[i], proximo = random.gauss(0.40, sigma), 2
                    elif proximo == 2:
                        vetx[i], proximo = random.gauss(0.60, sigma), 3
                    elif proximo == 3:
                        vetx[i] = random.gauss(0.75, sigma)
        return vetx, vety

    def gera_pontos_teste(quantidade_pontos, upper = True, anterior = False, sigma = 0.005):
        vetx = list(itertools.repeat(0., quantidade_pontos))
        vety = list(itertools.repeat(0., quantidade_pontos))

        espacamento = 1/(quantidade_pontos-2)
        ponto = np.copy(espacamento)
        for i in range(quantidade_pontos):
            if i == quantidade_pontos-1:
                vetx[quantidade_pontos-1], vety[quantidade_pontos-1] = 1., 0.
            elif i == quantidade_pontos-2:
                vetx[i] = random.gauss(ponto, sigma)
                ponto += espacamento
                if upper == False:
                    vety[i] = (random.uniform(0.04, -0.10))
                else:
                    vety[i] = (random.uniform(0., 0.10))
            elif i == quantidade_pontos-3 or i == quantidade_pontos-4:
                vetx[i] = random.gauss(ponto, sigma)
                ponto += espacamento
                if upper == False:
                    vety[i] = (random.uniform(0.04, -0.10))
                else:
                    vety[i] = (random.uniform(0., 0.2))
            elif i == 1:
                if anterior == False:
                    vety[1] = random.uniform(0.02, 0.15)
                    anterior = vety[1]
                else:
                    vety[1] = (random.uniform(-0.02, -0.08))
                    anterior = False
            elif i > 1:
                vetx[i] = random.gauss(ponto, sigma)
                ponto += espacamento
                if upper == False:
                    vety[i] = (random.uniform(-0.10, 0.))
                else:
                    vety[i] = (random.uniform(0.06, 0.2))

        return vetx, vety, anterior
    
    # função que gera de forma aleatória perfis (para os perfis iniciais)
    def gera_perfis(quant_perfis, sup = 8, inf = 9):
        perfis = []
        while len(perfis) < quant_perfis:
            print("ok")
            x_upper, y_upper, x_lower, y_lower, anterior = 0, 0, 0, 0, False
            x_upper, y_upper = otimizador.gera_pontos() # gera uma matriz de pontos superiores (aleatótios)
            x_lower, y_lower = otimizador.gera_pontos(False) # gera uma matriz de pontos inferiores (aleatórios)
            #if ((otimizador.verifica_cond(x_upper) == True) and (otimizador.verifica_cond(x_lower) == True) and (otimizador.verifica_cond(y_upper, True, True) == True) and (otimizador.verifica_cond(y_lower, True) == True)):
            perfil_1 = Perfil(x_upper, y_upper, x_lower, y_lower)
            if perfil_1.avalia_perfil() != "ERRO":
                perfis.append(perfil_1)

        ranking = otimizador.ranking_individuos(perfis)
        for i, perfil in enumerate(ranking):
            perfil.nome = str(i+1)
            perfil.geracao = '1'

        return ranking

    # função que avalia o quão bom é um perfil (com base no CD e no CL)
    
    # retorna a média da avaliação de um grupo de indivíduos 
    def media_avaliacao(individuos_populacao):
        soma = sum(i.avalia_perfil() for i in individuos_populacao if i.avalia_perfil() != "ERRO")
        return (soma/((len(individuos_populacao)*1.0)))

    #selecionar os melhores individuos de uma população para que a repodução ocorra 
    def sortear(matriz_avaliacao, indice_a_ignorar=-1): #indice_a_ignorar é um parametro que garante que não vai selecionar o mesmo elemento
        sigma = len(matriz_avaliacao)/2
        continua = True
        while continua:
            indice_sorteado = int(random.gauss(0, sigma))
            if indice_sorteado < 0: indice_sorteado = 0
            elif indice_sorteado > len(matriz_avaliacao)-1: indice_sorteado = len(matriz_avaliacao)-1
            if indice_sorteado != indice_a_ignorar:
                continua = False
        return indice_sorteado

    # função que seleciona o perfil pai e o perfil mãe para a próxima geração
    def selecao_roleta(pais):
        indice_pai = otimizador.sortear(pais)
        indice_mae = otimizador.sortear(pais, indice_pai)
        #print("Indice pai: ", indice_pai, "| Indice mãe: ", indice_mae)
        return indice_pai, indice_mae
    
    def evolui(pais, num_filhos, geracao, ind_mutacao = 0.4):
        #print(geracao)
        matriz_avaliacao = otimizador.ranking_individuos(pais)
        filhos = []

        while len(filhos) < num_filhos: # geração de filhos
            pai, mae = otimizador.selecao_roleta(matriz_avaliacao) # seleciona os genes dos pais e das mães, de forma pseudo aleatória
            perfil_pai, perfil_mae = matriz_avaliacao[pai], matriz_avaliacao[mae]
            if ((otimizador.verifica_cond(perfil_pai.x_upper) == True) and (otimizador.verifica_cond(perfil_mae.x_lower) == True) and (otimizador.verifica_cond(perfil_pai.y_upper, True, True) == True) and (otimizador.verifica_cond(perfil_mae.y_lower, True) == True)):
                filho = Perfil(perfil_pai.x_upper, perfil_pai.y_upper, perfil_mae.x_lower, perfil_mae.y_lower)
                if filho.avalia_perfil()!="ERRO":
                    filhos.append(filho)

        for i, perfil in enumerate(filhos):
            if ind_mutacao > random.random(): # verifica, de forma pseudo aleatória se alguma mutação irá ocorrer
                perfil_1 = otimizador.mutacao_mudado(perfil)
                filhos[i] = perfil_1

        ranking = otimizador.ranking_individuos(filhos)
        for i, perfil in enumerate(ranking):
            perfil.nome = str(i+1)
            perfil.geracao = str(geracao)
        return ranking

    def verifica_cond(vetx, y = False, upper = False):
        if y == True:
            if upper == True:
                for i in vetx:
                    if i < 0 or i > 0.2:
                        return False
            else:
                for i in vetx:
                    if i < -0.15 or i > 0.2:
                        return False
        else:
            for i in vetx:
                if i < 0 or i > 1:
                    return False
        return True

    def mutacao_mudado(perfil, sigma = 0.05): #ajustada para a sitação
        y_upper, y_lower = np.copy(perfil.y_upper), np.copy(perfil.y_lower)
        for i in range(1, len(y_upper)-2): # superior
            if i == len(y_upper)-2:
                y1 = otimizador.trunc_gauss(y_upper[i], sigma, 0.0, 0.10)
            elif i == len(y_upper)-3:
                y1 = otimizador.trunc_gauss(y_upper[i], sigma, 0.1, 0.10)
            elif i == 1: 
                y1 = otimizador.trunc_gauss(y_upper[i], sigma, 0.02, 0.08)
            else:
                y1 = otimizador.trunc_gauss(y_upper[i], sigma, 0.15, 0.23)
            y_upper[i] = y1

        for i in range(1, len(y_lower)-2): # inferiores
            if i == len(y_lower)-2:
                y2 = (otimizador.trunc_gauss(y_lower[i], sigma, -0.05, 0.10))
            elif i == 1:
                y2 = (otimizador.trunc_gauss(y_lower[i], sigma, -0.06, -0.01))
            elif i == 2 or i == 3:
                y2 = (otimizador.trunc_gauss(y_lower[i], sigma, -0.06, 0.0))
            else:
                y2 = (otimizador.trunc_gauss(y_lower[i], sigma, -0.06, 0.15))
            y_lower[i] = y2

        perfil_1 = Perfil(np.copy(perfil.x_upper), y_upper, np.copy(perfil.x_lower), y_lower)
        if perfil_1.avalia_perfil()!="ERRO":
            return perfil_1
        else: return otimizador.mutacao_mudado(perfil)
    
    def mutacao(perfil, sigma = 0.05):
        y_upper, y_lower = np.copy(perfil.y_upper), np.copy(perfil.y_lower)
        for i in range(2, len(y_upper)-1): # superior
            y1 = otimizador.trunc_gauss(y_upper[i], sigma, 0.05, 0.2)
            y_upper[i] = y1
        for i in range(2, len(y_lower)-1): # inferiores
            if i >= len(y_lower)-3:
                y2 = (otimizador.trunc_gauss(y_lower[i], sigma, -0.07, 0.05))
            else:
                y2 = (otimizador.trunc_gauss(y_lower[i], sigma, -0.15, 0.03))
            y_lower[i] = y2
        perfil_1 = Perfil(np.copy(perfil.x_upper), y_upper, np.copy(perfil.x_lower), y_lower)
        if perfil_1.avalia_perfil()!="ERRO":
            return perfil_1
        else: return otimizador.mutacao(perfil)

    # método que retorna o melhor individuo de uma população (com base em sua avaliacao)
    # avaliacao sendo realizada epenas a partir do cl (cl mais alto)
    def ranking_individuos(populacao):
        ranking_perfis = sorted(populacao, key=attrgetter('cl'), reverse=True)
        return ranking_perfis

    # função gaussiana truncada entre um intervalo (tilizada para o sortério pseudo aleatório de indivíduos)
    def trunc_gauss(mu, sigma, bottom, top):
        a = random.gauss(mu, sigma)
        if a >= top:
            return top
        if a <= bottom:
            return bottom
        return a
    
    def avalia_geracao(perfis):
        ranking = otimizador.ranking_individuos(perfis)
        anteriores = []
        anteriores.append(ranking[0])
        j=0
        for i in range(1, len(ranking)-1):
            if ranking[i] == anteriores[j]:
                anteriores.append(ranking[i])
                j += 1
            if len(anteriores)>3:
                return True
        return False