import matplotlib.pyplot as plt
from perfil import perfil_info
import itertools
import numpy as np
import random

class otimizador:

    def __init__(self, retorno) -> None:
        self.retorno = retorno
        #self.new_method()

    # método que gera pontos no palno x e y para serem utilizados na construção de um perfil com o método de Bezier
    # sendo que upper é para definir se os pontos serão nos quadrantes superiores ou inferiores do plano cartesiano
    def gera_pontos(quantidade_pontos, upper = True, anterior = False, sigma = 0.01):
        vetx = list(itertools.repeat(0., quantidade_pontos))
        vety = list(itertools.repeat(0., quantidade_pontos))
        espacamento = 1/(quantidade_pontos-2)
        ponto = espacamento
        for i in range(quantidade_pontos):
            if i == quantidade_pontos-1:
                vetx[quantidade_pontos-1], vety[quantidade_pontos-1] = 1., 0.
            elif i == quantidade_pontos-2:
                vetx[i] = random.gauss(ponto, sigma)
                ponto += espacamento
                if upper == False:
                    vety[i] = -(random.uniform(0., 0.10))
                else:
                    vety[i] = (random.uniform(0., 0.10))
            elif i == 1:
                if anterior == False:
                    vety[1] = random.uniform(0.02, 0.09)
                    anterior = vety[1]
                else:
                    vety[1] = -(anterior)
                    anterior = False
            elif i > 1:
                vetx[i] = random.gauss(ponto, sigma)
                ponto += espacamento
                if upper == False:
                    vety[i] = -(random.uniform(0., 0.15))
                else:
                    vety[i] = (random.uniform(0., 0.15))

        return vetx, vety, anterior
    
    # função que gera de forma aleatória perfis (para os perfis iniciais)
    def gera_perfis(quant_perfis):
        perfis = []
        for i in range(1, quant_perfis):
            x_upper, y_upper, anterior = otimizador.gera_pontos(6) # gera uma matriz de pontos superiores (aleatótios)
            x_lower, y_lower, anterior = otimizador.gera_pontos(8, False, anterior) # gera uma matriz de pontos inferiores (aleatórios)
            perfil_1 = perfil_info(x_upper, y_upper, x_lower, y_lower)
            perfis.append(perfil_1)
        return perfis

    # função que avalia o quão bom é um perfil (com base no CD e no CL)
    def avalia_perfil(individuo):
        try:
            cl, cd = individuo.getparametros_perfil()
            if cd < 0:
                avaliacao = "ERRO"
            else:
                avaliacao = abs(cl) - cd
        except:
            avaliacao = "ERRO"
        return avaliacao
    
    # retorna a média da avaliação de um grupo de indivíduos 
    def media_avaliacao(individuos_populacao):
        soma = sum(otimizador.avalia_perfil(i) for i in individuos_populacao if otimizador.avalia_perfil(i) != "ERRO")
        return (soma/((len(individuos_populacao)*1.0)))

    #selecionar os melhores individuos de uma população para que a repodução ocorra 
    def sortear(matriz_avaliacao, indice_a_ignorar=-1, sigma = 5): #indice_a_ignorar é um parametro que garante que não vai selecionar o mesmo elemento
        continua = True
        while continua:
            indice_sorteado = int(random.gauss(5, sigma))
            if indice_sorteado < 0: indice_sorteado = 0
            elif indice_sorteado > len(matriz_avaliacao[1])-1: indice_sorteado = len(matriz_avaliacao[1])-1
            if indice_sorteado != indice_a_ignorar:
                continua = False
        return indice_sorteado

    # função que seleciona o perfil pai e o perfil mãe para a próxima geração
    def selecao_roleta(pais):
        indice_pai = otimizador.sortear(pais)
        indice_mae = otimizador.sortear(pais, indice_pai)
        return indice_pai, indice_mae
    
    def evolui(pais, num_filhos, ind_mutacao = 0.05):
        matriz_avaliacao = otimizador.ranking_individuos(pais)
        filhos = []

        while len(filhos) < num_filhos: # geração de filhos
            pai, mae = otimizador.selecao_roleta(matriz_avaliacao) # seleciona os genes dos pais e das mães, de forma pseudo aleatória
            perfil_pai, perfil_mae = matriz_avaliacao[1][pai], matriz_avaliacao[1][mae]
            filho = perfil_info(perfil_pai.x_upper, perfil_pai.y_upper, perfil_mae.x_lower, perfil_mae.y_lower)
            filhos.append(filho)

        for perfil in filhos:
            if ind_mutacao > random.random(): # verifica, de forma pseudo aleatória se alguma mutação irá ocorrer
                perfil = otimizador.mutacao(perfil)
        return filhos

    def mutacao(perfil, sigma = 0.05):
        y_upper, x_upper = perfil.y_upper, perfil.x_upper
        y_lower, x_lower = perfil.y_lower, perfil.y_lower
        for i in range(2, len(y_upper)-1):
            y_upper[i] = otimizador.trunc_gauss(y_upper[i], sigma, 0., 0.15)
            x_upper[i] = otimizador.trunc_gauss(x_upper[i], sigma, 0., 0.15)
        for i in range(10, len(y_lower)-10):
            y_lower[i] = otimizador.trunc_gauss(y_lower[i], sigma, -0.15, 0.)
            x_lower[i] = otimizador.trunc_gauss(x_lower[i], sigma, -0.15, 0.)
        perfil = perfil_info(x_upper, y_upper, x_lower, y_lower)
        return perfil

    # método que retorna o melhor individuo de uma população (com base em sua avaliacao)
    def ranking_individuos(populacao):
        perfis = [[otimizador.avalia_perfil(i), i] for i in populacao if otimizador.avalia_perfil(i)!= "ERRO"]
        print(perfis)
        perfis = sorted(perfis, reverse=True)
        valores = list(zip(*perfis))
        return valores

    # função gaussiana truncada entre um intervalo (tilizada para o sortério pseudo aleatório de indivíduos)
    def trunc_gauss(mu, sigma, bottom, top):
        a = random.gauss(mu, sigma)
        if a >= top:
            return top
        if a <= bottom:
            return bottom
        return a
