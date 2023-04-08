# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 22:21:15 2023

@author: AM
"""

import matplotlib.pyplot as plt
import numpy as np
import csv

# FFT

dados: list[any]  =  []


# *********************
# * LEITURA DOS DADOS *
# *********************
path  =  "data_files/sinaisvitais003 100dias DV2 RAxxx9.txt"

with open(path,'r',newline = '') as ARQUIVO:
 d  =  csv.reader(ARQUIVO)
 dd = list(d)
 for i in range(0,len(dd)):
  p = dd[i][0]  
  palavras = p.split("\t")
  dados.append({"HORA":palavras[0],"BATIMENTO":palavras[1],"PRESSAO":palavras[2],"TEMPERATURA":palavras[3]})
  
  
# **********************************
# * SEPARAR OS CAMPOS PARA ANALISE *
# **********************************
hora = []
batimento = []
pressao = []
temperatura = []

for i in range(0,len(dados)):
    hora.append(dados[i]["HORA"])
    batimento.append(float(dados[i]["BATIMENTO"]))
    pressao.append(float(dados[i]["PRESSAO"]))
    temperatura.append(float(dados[i]["TEMPERATURA"]))



# ************************************
# * CALCUALR A MEDIA DE DOIS VALORES *
# ************************************
def media(v1: float, v2: float) -> float:
  return (v1 + v2)/2

#****************************************
# PRE-PROCESSAMENTO
# 0  <  =  Batimento  <  =  200
# 0  <  =  pressao  <  =  25
# 0  <  =  temperatura  <  =  50 
#****************************************
for i in range(1,len(dados)-1):
    if (batimento[i] < 0) or (batimento[i] > 200):
        batimento[i] = media(batimento[i-1],batimento[i + 1])
    if (pressao[i] < 0) or (pressao[i] > 25):
        pressao[i] = media(pressao[i-1],pressao[i + 1])
    if (temperatura[i] < 0) or (temperatura[i] > 50):
        temperatura[i] = media(temperatura[i-1],temperatura[i + 1])

        
#****************************************
# ESTATISTICA BASICA
#****************************************

somaBatimento: float = 0
mediaBatimento: float = 0
maxBatimento: float = -100
minBatimento: float = 100000

somaPressao: float = 0
mediaPressao: float = 0
maxPressao: float = -100
minPressao: float = 100000

somaTemperatura: float = 0
mediaTemperatura: float = 0
maxTemperatura: float = -100
minTemperatura: float = 100000

histoBatimento: list[float] = []
histoPressao: list[float] = []
histoTemperatura: list[float] = []

for i in range(0,100):
    histoBatimento.append(0)
    histoPressao.append(0)
    histoTemperatura.append(0)

for i in range(0,len(dados)):
  somaBatimento = somaBatimento + float(batimento[i])
  somaPressao = somaPressao + float(pressao[i])
  somaTemperatura = somaTemperatura + float(temperatura[i])
  
  if (float(batimento[i]) > maxBatimento):
      maxBatimento = float(batimento[i])
  if (float(pressao[i]) > maxPressao):
      maxPressao = float(pressao[i])
  if (float(temperatura[i]) > maxTemperatura):
      maxTemperatura = float(temperatura[i])
      
  if (float(batimento[i]) < minBatimento):
      minBatimento = float(batimento[i])
  if (float(pressao[i]) < minPressao):
      minPressao = float(pressao[i])
  if (float(temperatura[i]) < minTemperatura):
      minTemperatura = float(temperatura[i])
      
  histoBatimento[int(batimento[i])] += 1
  histoPressao[int(pressao[i])] += 1
  histoTemperatura[int(temperatura[i])] += 1
      
mediaBatimento = somaBatimento/len(dados)
mediaPressao = somaPressao/len(dados)
mediaTemperatura = somaTemperatura/len(dados)

print("**********************************")
print("TAMANHO DA AMOSTRA  =  ",len(dados))
print(" ")
print("BATIMENTO MÉDIO  = ",mediaBatimento)
print("BATIMENTO MÁXIMO  = ",maxBatimento)
print("BATIMENTO MÍNIMO  = ",minBatimento)
print(" ")
print("PRESSAO MÉDIA  = ",mediaPressao)
print("PRESSAO MÁXIMA  = ",maxPressao)
print("PRESSAO MÍNIMA  = ",minPressao)
print(" ")
print("TEMPERATURA MÉDIA  = ",mediaTemperatura)
print("TEMPERATURA MÁXIMA  = ",maxTemperatura)
print("TEMPERATURA MÍNIMA  = ",minTemperatura)


#HISTOGRAMA BATIMENTO CARDIACO
plt.hist(batimento)
plt.xlabel("BATIMENTO")
plt.ylabel("FREQUENCIA")
plt.show()

plt.plot(histoBatimento[int(minBatimento)-1:int(maxBatimento) + 2],color = 'darkblue')
xb = np.arange(int(minBatimento)-1,int(maxBatimento) + 2)
xb1 = np.arange(0,len(xb))
plt.xticks(xb1,xb,rotation = 'vertical')
plt.xlabel("BATIMENTO")
plt.ylabel("FREQUENCIA")
plt.show()

#HISTOGRAMA PRESSAO ARTERIAL
plt.hist(pressao)
plt.xlabel("PRESSAO")
plt.ylabel("FREQUENCIA")
plt.show()

plt.plot(histoPressao[int(minPressao)-1:int(maxPressao) + 2],color = 'darkgreen')
xp = np.arange(int(minPressao)-1,int(maxPressao) + 2)
xp1 = np.arange(0,len(xp))
plt.xticks(xp1,xp,rotation = 'vertical')
plt.xlabel("PRESSAO")
plt.ylabel("FREQUENCIA")
plt.show()

#HISTOGRAMA TEMPERATURA
plt.hist(temperatura)
plt.xlabel("TEMPERATURA")
plt.ylabel("FREQUENCIA")
plt.show()

tp = histoTemperatura[int(minTemperatura)-1:int(maxTemperatura) + 2]
plt.plot(tp,color = 'yellow')
xt = np.arange(int(minTemperatura)-1,int(maxTemperatura) + 2)
xt1 = np.arange(0,len(xt))
plt.xticks(xt1,xt,rotation = 'vertical')
plt.xlabel("TEMPERATURA")
plt.ylabel("FREQUENCIA")
plt.show()

# plt.plot(batimento,color = 'darkblue')
# x = np.arange(len(hora))
# plt.xticks(x,hora,rotation = 'vertical')
# plt.xlabel("HORA")
# plt.ylabel("BATIMENTO")
# plt.show()


# fig, ax  =  plt.subplots(figsize = (15,5))
# ax.plot(hora,batimento, 'o', label = 'BATIMENTO',color = 'darkblue')
# ax.plot(hora,pressao, 'd', label = 'PRESSAO',color = 'darkgreen')
# ax.plot(hora,temperatura, 'v', label = 'TEMPERATURA',color = 'yellow')
# #ax.set_xticks(np.arange(0,len(hora)),['0',"1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"])
# ax.set_xlabel('HORA')
# ax.legend();


# fig1, ax1  =  plt.subplots(figsize = (15,5))
# ax1.plot(hora,pressao, 'd', label = 'PRESSAO',color = 'darkblue')
# ax1.set_xlabel('HORA')
# ax1.set_ylabel('PRESSAO')
# ax1.legend();


# fig2,ax2  =  plt.subplots(figsize = (15,5))
# n, bins, patches  =  ax2.hist(batimento,color = 'darkblue') 
# ax2.set_xlabel('BATIMENTO')
# ax2.set_ylabel('OCORRENCIAS')
# ax2.legend();






