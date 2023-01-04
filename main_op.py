from Otimiza_Classe import otimizador
from perfil import perfil_info

perfis = otimizador.gera_perfis(10)

#perfis[0].informacoes_perfil()
print("ok")
#print("Parametros do melhor perfil: ", otimizador.melhor_individuo_geracao(perfis).getparametros_perfil())
print("Parametros do perfil 1: ", perfis[0].getparametros_perfil())
perfis2 = otimizador.evolui(perfis, 10)
for i in range(0, len(perfis2)-1):
    print(i)
    print("Parametros de um perfil: ",perfis2[i].getparametros_perfil())
#melhor = otimizador.melhor_individuo_geracao(perfis)
#melhor2 = otimizador.melhor_individuo_geracao(perfis2)
# for i in range(0, len(melhor[0])-1):
#     print("Valor do melhor ",i ," :", melhor[0][i])
#     print("Info perfis: ", melhor[1][i].getparametros_perfil())
# melhor[1][0].informacoes_perfil()
# melhor2[1][0].getparametros_perfil()
#perfis2 = otimizador.evolui(perfis, 5)
#print(otimizador.avalia_perfil(otimizador.melhor_individuo_geracao(perfis)))
#print(otimizador.avalia_perfil(otimizador.melhor_individuo_geracao(perfis2)))