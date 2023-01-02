import matplotlib.pyplot as plt
from perfil import perfil_info
import itertools
import numpy as np
import random

class otimizador:

    def __init__(self, retorno) -> None:
        self.retorno = retorno
        #self.new_method()

    def gera_pontos(quantidade_pontos, upper = True, sigma = 0.01):
        vetx = list(itertools.repeat(0., quantidade_pontos))
        vety = list(itertools.repeat(0., quantidade_pontos))
        espacamento = 1/quantidade_pontos
        ponto = espacamento
        for i in range(quantidade_pontos):
            if i == quantidade_pontos-1:
                vetx[quantidade_pontos-1], vety[quantidade_pontos-1] = 1., 0.
            elif i >= 1:
                vetx[i] = random.gauss(ponto, sigma)
                ponto += espacamento
                if upper == False:
                    vety[i] = -(random.uniform(0., 0.15))
                else:
                    vety[i] = (random.uniform(0., 0.15))
        return vetx, vety
    
    def gera_perfis(quant_perfis):
        perfis = []
        for i in range(1, quant_perfis):
            #print("ok")
            x_upper, y_upper = otimizador.gera_pontos(6) # gera uma matriz de pontos superiores (aleatótios)
            x_lower, y_lower = otimizador.gera_pontos(8, False) # gera uma matriz de pontos inferiores (aleatórios)
            perfil_1 = perfil_info(x_upper, y_upper, x_lower, y_lower)
            perfis.append(perfil_1)
        return perfis

    def avalia_perfil(individuo):
        cl, cd = individuo.getparametros_perfil()
        if cd < 0:
            avaliacao = "E"
        else:
            avaliacao = abs(cl) - cd
        return avaliacao
    
    def media_avaliacao(individuos_populacao):
        soma = sum(otimizador.avalia_perfil(i) for i in individuos_populacao)
        return (soma/((len(individuos_populacao)*1.0)))
        
    # def avaliacao(individuo, peso_maximo, volume_maximo, objetos):
    #     retorno = 0
    #     peso_tot, val_tot, volume_tot = 0, 0, 0
    #     for i, x in enumerate(individuo):
    #         peso_tot += (individuo[i] * objetos[i][0])
    #         val_tot += (individuo[i] * objetos[i][1])
    #         volume_tot += (individuo[i] * objetos[i][2])
    #     if (peso_maximo - peso_tot) < 0 or (volume_maximo - volume_tot) < 0:
    #         return 0
    #     else:
    #         return val_tot
        
    # def media_avaliacao(individuos_populacao, peso_maximo, volume_maximo, objetos):
    #     soma = sum(otimizador.avaliacao(i, peso_maximo, volume_maximo, objetos) for i in individuos_populacao if otimizador.avaliacao(i, peso_maximo, volume_maximo, objetos)>=0)
    #     return (soma/((len(individuos_populacao)*1.0)))

    #selecionar os melhores individuos de uma população para 

    def sortear(matriz_avaliacao, indice_a_ignorar=-1, sigma = 1): #indice_a_ignorar é um parametro que garante que não vai selecionar o mesmo elemento
        indice_sorteado = int(random.gauss(5, sigma))
        if indice_sorteado < 0: indice_sorteado = 0
        elif indice_sorteado > len(matriz_avaliacao[1])-1: indice_sorteado = len(matriz_avaliacao[1])-1
        if indice_sorteado == indice_a_ignorar:
            indice = otimizador.sortear(matriz_avaliacao, indice_a_ignorar)
        return indice

    def selecao_roleta(pais):
        indice_pai = otimizador.sortear(pais)
        indice_mae = otimizador.sortear(pais, indice_pai)
        return indice_pai, indice_mae
    
    def evolui(pais, num_filhos, ind_mutacao = 0.05):
        matriz_avalizacao = np.zeros((len(pais), 2))
        for i in range(pais):
            matriz_avalizacao[i, 0], matriz_avalizacao[i, 1] = otimizador.avalia_perfil(pais[i]), pais[i]
        sorted(matriz_avalizacao[0], reverse=True)
        filhos = []

        while len(filhos) < num_filhos: # geração de filhos
            pai, mae = otimizador.selecao_roleta(matriz_avalizacao) # seleciona os genes dos pais e das mães, de forma pseudo aleatória
            perfil_pai, perfil_mae = matriz_avalizacao[pai, 1], matriz_avalizacao[mae, 1]
            filho = perfil_info(perfil_pai.x_upper, perfil_mae.y_upper, perfil_mae.x_lower, perfil_pai.y_lower)
            filhos.append(filho)

        for perfil in filhos:
            if ind_mutacao > random(): # verifica, de forma pseudo aleatória se alguma mutação irá ocorrer
                mutacao = random.getrandbits() # seleciona aleatoriamente no individuo um gene a ser mudado
                if mutacao == 1:
                    y_upper = otimizador.trunc_gauss(perfil.y_upper, ind_mutacao, 0, 15)
                    perfil = perfil_info(perfil.x_upper, y_upper, perfil.x_lower, perfil.y_lower)
                else:
                    y_lower = otimizador.trunc_gauss(perfil.y_lower, ind_mutacao, -15, 0)
                    perfil = perfil_info(perfil.x_upper, perfil.y_upper, perfil.x_lower, y_lower)

        return filhos

    def melhor_individuo_geracao(populacao_mochilas, peso_maximo, vomume_maximo, objetos):
        anterior = 0
        proximo = 0
        individuo = populacao_mochilas[0]
        for i in range(0, len(populacao_mochilas)):
            proximo = otimizador.avaliacao(populacao_mochilas[i], peso_maximo, vomume_maximo, objetos)
            if proximo > anterior:
                anterior = proximo
                individuo = populacao_mochilas[i]
        return anterior, individuo

    def valores_armazenados(individuo):
        soma_valor, soma_volume, soma_peso = 0, 0, 0
        for i in range(0, len(individuo)):
            #print(individuo[i])
            if individuo[i] == 1:
                soma_peso += otimizador.objetos[i][0]
                soma_volume += otimizador.objetos[i][2]
                soma_valor += otimizador.objetos[i][1]
        return soma_peso, soma_volume, soma_valor

    def trunc_gauss(mu, sigma, bottom, top):
        a = random.gauss(mu, sigma)
        if a >= top:
            return top
        if a <= bottom:
            return bottom
        return a
