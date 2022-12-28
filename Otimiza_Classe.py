import matplotlib.pyplot as plt
from perfil import perfil_info
import itertools
import numpy as np
import random

class otimizador:

    def __init__(self, retorno) -> None:
        self.retorno = retorno
        #self.new_method()

    # def individuos(quant_objetos):
    #     return [random.getrandbits(1) for i in range(quant_objetos)]

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
            x_upper, y_upper = otimizador.gera_pontos(6) # gera uma matriz de pontos superiores (aleatótios)
            x_lower, y_lower = otimizador.gera_pontos(8, False) # gera uma matriz de pontos inferiores (aleatórios)
            perfil_1 = perfil_info(x_upper, y_upper, x_lower, y_lower)
            perfis.append(perfil_1)
        return perfis

    # def populacao(n_filhos, quant_objetos):
    #     return [otimizador.individuos(quant_objetos) for i in range(n_filhos)]

    # def gera_perfis(n_filhos, quant_perfis):
    #     return [otimizador.gera_perfil(quant_perfis) for i in range(n_filhos)]
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

    def sortear(avaliacao_total, valores, indice_a_ignorar=-1): #indice_a_ignorar é um parametro que garante que não vai selecionar o mesmo elemento
        roleta, acumulado, valor_sorteado = [], 0, random() # sorteia um valor a partir da função random() (entre 0 e 1)
        print("Numero sorteado ", valor_sorteado)
        if indice_a_ignorar != -1: # Desconta do total o valor que sera retirado da roleta
            avaliacao_total -= valores[0][indice_a_ignorar]
        for indice, i in enumerate(valores[0]): # indice é a posição do valor na tupla de valores, i é o valore da avaliação
            if indice_a_ignorar == indice: # ignora o valor ja utilizado na roleta
                #print("ok", indice)
                continue
            #print("ok", indice)
            acumulado += i # valor da avaliação é somado com o valor calculado
            roleta.append(acumulado/avaliacao_total) # valor é colocado na última posição da 'roleta'
            #print("roleta: ", roleta, " | valor da iteração atual: ", i)
            # temos que se o valor da iteração atual somado com os valores das iteração anteriores (que está armazenado na variável acomulado), dividido pela soma de todas
            # as avaliações dos pais for maior que o valor que foi sorteado, então a "roleta irá sortear" esse indice
            if roleta[-1] >= valor_sorteado: # se o ultimo elemento de roleta for maior que o valor sorteado
                print("Valor sorteado: ", i, " | indice: ",indice)
                return indice
    

    def selecao_roleta(pais):
        # função que sorteia um indicie de pai e de mãe a ser analisado
    
        valores = list(zip(*pais)) # organiza os dados de uma geração passada (pais) em duas tuplas, sendo que a primeria contém os dados de avaliação de cada individuo (valor de fitness)
        # e a sengunda contém os valoes dos genes (quais objetos estão nessas mochilas pais)
        print("Printando os val: ", valores)
        avaliacao_total = sum(valores[0]) # o somatótio de todas as avaliaçãoes dos indivíduos (somatório da primeira tupla)
        #print("valores: ", valores[0])

        indice_pai = otimizador.sortear(avaliacao_total, valores) # sorteia, de forma pseudo aleatória os gesnes dos pais
        indice_mae = otimizador.sortear(avaliacao_total, valores, indice_pai)

        pai = valores[1][indice_pai] # selecionando a mochila pai e a mochila mãe
        mae = valores[1][indice_mae]
        #print("pai e mae ", pai, mae)
        
        return pai, mae
    
    def evolui(individuos_populacao, peso_maximo, volume_maximo, objetos, num_filhos, ind_mutacao = 0.05):
        pais = [[otimizador.avaliacao(i, peso_maximo, volume_maximo, objetos), i] for i in individuos_populacao if otimizador.avaliacao(i, peso_maximo, volume_maximo, objetos)>= 0]
        #print(pais)
        pais.sort(reverse=True) # organiza em ordem decrescente pela avaliação
        #print("Após a organização")
        print(pais, "\n")
        filhos = []

        while len(filhos) < num_filhos: # geração de filhos
            pai, mae = otimizador.selecao_roleta(pais) # seleciona os genes dos pais e das mães, de forma pseudo aleatória
            meio = len(pai)//2 # divisão que retorna um numero inteiro 
            filho = pai[:meio] + mae[meio:] # o filho é gerado a partir da metade dos genes do pai e metade dos genes da mae
            filhos.append(filho) # os genes do filho são colocados na lista de filhos

        for mochila in filhos:
            if ind_mutacao > random(): # verifica, de forma pseudo aleatória se alguma mutação irá ocorrer
                posicao_mutacao = random.randint(0, len(mochila)-1) # seleciona aleatoriamente no individuo um gene a ser mudado
                if mochila[posicao_mutacao] == 1: # se o gene estiver em um muda para zero e vice-versa 
                    mochila[posicao_mutacao] = 0
                else:
                    mochila[posicao_mutacao] = 1
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
