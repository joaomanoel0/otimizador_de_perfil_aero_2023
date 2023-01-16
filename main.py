from Otimiza_Classe import otimizador
from perfil import perfil_info
import numpy as np

num_geracoes = 2
num_filhos = 5

perfis = otimizador.gera_perfis(num_filhos)
for perfil in perfis:
    perfil.salvar_perfil()
perfis_1 = np.copy(perfis)

for i in range(num_geracoes):
    perfis = otimizador.evolui(perfis_1, num_filhos, i+1)
    perfis_1 = np.copy(perfis)
    for perfil in perfis_1:
        perfil.salvar_perfil()