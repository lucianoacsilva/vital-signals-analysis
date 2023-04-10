# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 16:11:39 2023

@author: Luan
"""

# =============================================================================
# ================================ BIBLIOTECAS ================================
# =============================================================================

import os
import csv
import statistics
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# =============================================================================

# ================================== ETAPA 1 ==================================

# =============================================================================
# ============================= LEITURA DOS DADOS =============================
# =============================================================================

dados = []

path = os.getcwd()+os.sep+"sinaisvitais003 100dias DV2 RAxxx4.txt"
with open(path,'r',newline='') as ARQUIVO:
    d = csv.reader(ARQUIVO)
    dd = list(d)
    for i in range(0,len(dd)):
        p = dd[i][0]  
        palavras = p.split("\t")
        dados.append({"HORA":palavras[0],"BATIMENTO":palavras[1],
                      "PRESSAO":palavras[2],"TEMPERATURA":palavras[3]})

# Criar o DataFrame
df = pd.DataFrame(data = dados, dtype=float)

# =============================================================================
# ======================== TRATAR VALORES INCOERENTES =========================
# =============================================================================

# ================================= Batimento =================================
# Excluir valores fora da faixa
#df = df.loc[df['BATIMENTO'] <= 100]

# Substituir pela média
#for j in range(len(dd)):
#    if df['BATIMENTO'][j] > 100:
#        df['BATIMENTO'].replace(df['BATIMENTO'][j], np.NaN, inplace=True)

#df['BATIMENTO'].fillna(df['BATIMENTO'].mean(), inplace=True)

# Substituir pela média entre o anterior e posterior
#for j in range(len(dd)):
#    if df['BATIMENTO'][j] > 100:
#        m_aux = (df['BATIMENTO'][j-1]+df['BATIMENTO'][j+1])/2
#        df['BATIMENTO'].replace(df['BATIMENTO'][j], m_aux, inplace=True)
        
# ================================== Pressão ==================================
# Excluir valores fora da faixa
#df = df.loc[df['PRESSAO'] <= 20]

# Substituir pela média
#for j in range(len(dd)):
#    if df['PRESSAO'][j] > 20:
#        df['PRESSAO'].replace(df['PRESSAO'][j], np.NaN, inplace=True)

#df['PRESSAO'].fillna(df['PRESSAO'].mean(), inplace=True)

# Substituir pela média entre o anterior e posterior
#for j in range(len(dd)):
#    if df['PRESSAO'][j] > 20:
#        m_aux = (df['PRESSAO'][j-1]+df['PRESSAO'][j+1])/2
#        df['PRESSAO'].replace(df['PRESSAO'][j], m_aux, inplace=True)
        
# ================================ Tempertura =================================
# Excluir valores fora da faixa
#df = df.loc[df['TEMPERATURA'] <= 40]

# Substituir pela média
#for j in range(len(dd)):
#    if df['TEMPERATURA'][j] > 40:
#        df['TEMPERATURA'].replace(df['TEMPERATURA'][j], np.NaN, inplace=True)

#df['TEMPERATURA'].fillna(df['TEMPERATURA'].mean(), inplace=True)

# Substituir pela média entre o anterior e posterior
#for j in range(len(dd)):
#    if df['TEMPERATURA'][j] > 40:
#        m_aux = (df['TEMPERATURA'][j-1]+df['TEMPERATURA'][j+1])/2
#        df['TEMPERATURA'].replace(df['TEMPERATURA'][j], m_aux, inplace=True)

# =============================================================================
# ============= PLOTAGENS DOS SINAIS E DOS HISTOGRAMAS DOS DADOS ==============
# =============================================================================

# Plotar o sinal do batimento cardíaco
plt.plot(df['BATIMENTO'],color='darkblue')
plt.grid()
plt.title("Sinal do Batimento Cardiaco")
plt.xlabel("AMOSTRAS")
plt.ylabel("BATIMENTO CARDIACO")
plt.show()

# Plotar o sinal da pressão arterial
plt.plot(df['PRESSAO'],color='darkblue')
plt.grid()
plt.title("Sinal da Pressão Arterial")
plt.xlabel("AMOSTRAS")
plt.ylabel("PRESSÃO ARTERIAL")
plt.show()

# Plotar o sinal da temperatura
plt.plot(df['TEMPERATURA'],color='darkblue')
plt.grid()
plt.title("Sinal da Temperatura Corporal")
plt.xlabel("AMOSTRAS")
plt.ylabel("TEMPERATURA CORPORAL")
plt.show()

# Plotar os histogramas dos dados
plt.figure()
plt.grid()
plt.title("Histograma do Batimento Cardiaco")
sns.histplot(data=df, x="BATIMENTO", bins = 30)
plt.figure()
plt.grid()
plt.title("Histograma da Pressão Arterial")
sns.histplot(data=df, x="PRESSAO", bins = 30)
plt.figure()
plt.grid()
plt.title("Histograma da Temperatura Corporal")
sns.histplot(data=df, x="TEMPERATURA", bins = 30)

# =============================================================================
# ============================ ANÁLISE DO DATASET =============================
# ========================== 0 <= Batimento <= 100 ============================
# ============================ 0 <= Pressão <= 20 =============================
# ========================== 0 <= Temperatura <= 40 ===========================
# =============================================================================

# Verificar se há valores faltantes
print("\nQuantidade de valores faltantes:")
print(df.isnull().sum())

# Valores fora da faixa de análise padrão
valores_fora = pd.DataFrame()
# Contar valores fora da faixa, e inserir em um DataFrame
valores_fora[''] = ['Batimento','Pressão','Temperatura']
valores_fora['Valores abaixo da faixa'] = [sum(i <= 0 for i in df["BATIMENTO"]),
                                           sum(i <= 0 for i in df["PRESSAO"]),
                                           sum(i <= 0 for i in df["TEMPERATURA"])]

valores_fora['Valores acima da faixa'] = [sum(i >= 100 for i in df["BATIMENTO"]),
                                          sum(i >= 20 for i in df["PRESSAO"]),
                                          sum(i >= 40 for i in df["TEMPERATURA"])] 

valores_fora['Total'] = valores_fora['Valores abaixo da faixa'] + valores_fora['Valores acima da faixa']
                                     
print("\nQuantidade de valores fora da faixa:")
print(valores_fora.to_string(index = False))

# ================================== ETAPA 2 ==================================

# Correlação dos 100 dias de coleta de dados
n = 1

df_correlacao = pd.DataFrame()

c_HORAxBATIMENTO = []
c_HORAxPRESSAO = []
c_HORAxTEMPERATURA = []
c_BATIMENTOxPRESSAO = []
c_BATIMENTOxTEMPERATURA = []
c_TEMPERATURAxPRESSAO  = []

# Segmentação do Datasete em 100 pacotes com 24 amostras
for k in range(0,2400,24):
    
    # Cálculo da correlação de cada pacote de dados
    correlacao = df[k:k+24].corr(method ='pearson')

    c_HORAxBATIMENTO.append(correlacao['HORA'][1])
    c_HORAxPRESSAO.append(correlacao['HORA'][2])
    c_HORAxTEMPERATURA.append(correlacao['HORA'][3])
    c_BATIMENTOxPRESSAO.append(correlacao['BATIMENTO'][2])
    c_BATIMENTOxTEMPERATURA.append(correlacao['BATIMENTO'][3])
    c_TEMPERATURAxPRESSAO.append(correlacao['TEMPERATURA'][2])

df_correlacao['Hora x Batimento'] = c_HORAxBATIMENTO
df_correlacao['Hora x Pressão'] = c_HORAxPRESSAO
df_correlacao['Hora x Temperatura'] =  c_HORAxTEMPERATURA
df_correlacao['Batimento x Pressão'] = c_BATIMENTOxPRESSAO
df_correlacao['Batimento x Temperatura'] = c_BATIMENTOxTEMPERATURA
df_correlacao['Temperatura x Pressão'] = c_TEMPERATURAxPRESSAO

# ================================== ETAPA 3 ==================================

# Plotar a correlação entre os dados
plt.figure()
plt.grid()
plt.title("Correlação entre os dados")
plt.xlabel("Dias")
plt.ylabel("Correlação")
plt.plot(c_BATIMENTOxPRESSAO, color = 'g', label = 'Batimento x Pressão')
plt.plot(c_BATIMENTOxTEMPERATURA, color = 'b', label = 'Batimento x Temperatura')
plt.plot(c_TEMPERATURAxPRESSAO, color = 'r', label = 'Temperatura x Pressão')
plt.legend()

# ================================== ETAPA 4 ==================================

# =============================================================================
# ==================== ESTATÍSTICA DESCRITIVA DO PROBLEMA =====================
# =============================================================================

estatistica_Batimento = pd.DataFrame()
estatistica_Pressao = pd.DataFrame()
estatistica_Temperatura = pd.DataFrame()

media = np.zeros((100,3))
madiana = np.zeros((100,3))
moda = np.zeros((100,3))
desvio_padrao = np.zeros((100,3))
p = 0

# Segmentação do Datasete em 100 pacotes com 24 amostras
for k in range(0,2400,24):

    # Cálculo da média, madiana, e devio padrão
    aux = df[k:k+24].describe()

    media[p][0] = aux['BATIMENTO'][1]
    media[p][1] = aux['PRESSAO'][1]
    media[p][2] = aux['TEMPERATURA'][1]
    
    madiana[p][0] = aux['BATIMENTO'][5]
    madiana[p][1] = aux['PRESSAO'][5]
    madiana[p][2] = aux['TEMPERATURA'][5]
    
    desvio_padrao[p][0] = aux['BATIMENTO'][2]
    desvio_padrao[p][1] = aux['PRESSAO'][2]
    desvio_padrao[p][2] = aux['TEMPERATURA'][2]
    
    moda[p][0] = statistics.mode(df['BATIMENTO'][k:k+24])
    moda[p][1] = statistics.mode(df['PRESSAO'][k:k+24])
    moda[p][2] = statistics.mode(df['TEMPERATURA'][k:k+24])
    
    p = p + 1
    
estatistica_Batimento['Média'] = media[:,0]
estatistica_Batimento['Mediana'] = madiana[:,0]
estatistica_Batimento['Moda'] = moda[:,0]
estatistica_Batimento['Desvio Padrão'] = desvio_padrao[:,0]

estatistica_Pressao['Média'] = media[:,1]
estatistica_Pressao['Mediana'] = madiana[:,1]
estatistica_Pressao['Moda'] = moda[:,1]
estatistica_Pressao['Desvio Padrão'] = desvio_padrao[:,1]

estatistica_Temperatura['Média'] = media[:,2]
estatistica_Temperatura['Mediana'] = madiana[:,2]
estatistica_Temperatura['Moda'] = moda[:,2]
estatistica_Temperatura['Desvio Padrão'] = desvio_padrao[:,2]

# =============================================================================
# ============================= TOMADA DE DECISÃO =============================
# =============================================================================

diagnostico = pd.DataFrame()
d = []
# Diagnóstico do Batimento Cardíaco
for m in estatistica_Batimento['Média']:
    
    if (m < 100):
        d.append("Normal")
    else:
        d.append("Preocupante")

diagnostico['Batimento Cardíaco'] = d

d.clear()

# Diagnóstico da Pressão Arterial
for m in estatistica_Pressao['Média']:
    
    if (m < 9):
        d.append("Pressão Baixa")
    elif ((m >= 9) and (m <= 12)):
        d.append("Normal")
    elif ((m > 12) and (m < 14)):
        d.append("Pré-Hipertensão")
    elif ((m >= 14) and (m < 16)):
        d.append("Hipertensão Estágio 1")
    elif ((m >= 16) and (m < 18)):
        d.append("Hipertensão Estágio 2")
    elif (m >= 18):
        d.append("Crise Hipertensiva")

diagnostico['Pressão Arterial'] = d

d.clear()

# Diagnóstico da Temperatura Corporal
for m in estatistica_Temperatura['Média']:
    
    if (m < 35):
        d.append("Hipotermia")
    elif ((m > 35) and (m <= 37.7)):
        d.append("Normal")
    elif ((m > 37.7) and (m <= 39.5)):
        d.append("Febre")
    elif ((m > 39.5) and (m <= 41)):
        d.append("Febre Alta")
    elif (m > 41):
        d.append("Hipertemia")

diagnostico['Temperatura Corporal'] = d

d.clear()

print("\n*************************************************************\n")
print("Diagnóstico: \n")
print("Batimento Cardíaco: ", statistics.mode(diagnostico['Batimento Cardíaco']))
print("Pressão Arterial: ", statistics.mode(diagnostico['Pressão Arterial']))
print("Temperatura Corporal: ", statistics.mode(diagnostico['Temperatura Corporal']))