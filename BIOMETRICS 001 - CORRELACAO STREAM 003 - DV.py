# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 20:45:54 2022

@author: AM
"""

# CARREGAR AS BIBLIOTECA
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import csv
from pandas import read_csv
from pandas import set_option


# VALORES DO ARQUIVO
dados=[]


# LISTA DE PADROES
LPD=[]
LPD.append("CORACAO OK")

# LER DADOS DO ARQUIVO PADRAO.TXT
# VETOR PARA ARMAZENAMENTO DOS DADOS
# *********************
# * LEITURA DOS DADOS *
# *********************
import csv
path = "D:\\PUC-CAMPINAS\\ESTUDOS AVANCADOS BANCO DE DADOS\\AULAS\\AULA003 ESTATISTICA\\sinaisvitais003 100dias DV2.txt"
with open(path,'r',newline='') as ARQUIVO:
 d = csv.reader(ARQUIVO)
 dd=list(d)
 for i in range(0,len(dd)):
  p=dd[i][0]  
  palavras=p.split("\t")
  dados.append({"HORA":palavras[0],"BATIMENTO":palavras[1],"PRESSAO":palavras[2],"TEMPERATURA":palavras[3]})
  
 # ************************************************* 
 # CALCULO DA CORRELACAO ENTRE OS TRES PARAMETROS 
 # *************************************************
 print("\n\n*************************************************")
 print("DADOS DE CORRELAÇÃO ENTRE OS TRÊS PARÂMETROS")
 print("*************************************************")
 auxDF=[]
 # z VARIAVEL AUXILIAR PARA MONTAGEM DO DATAFRAME
 auxDF+=[(float(float(dados[j]["BATIMENTO"])),float(dados[j]["PRESSAO"]),float(dados[j]["TEMPERATURA"])) for j in range(0,len(dados))]
 DataFrame=[]
 # MONTAGEM
 DataFrame = pd.DataFrame(auxDF,columns=["BATIMENTO", "PRESSAO","TEMPERATURA"])
 print(DataFrame.corr())    
 
 print("\n*************************************************")
 print("DADOS ESTATÍSTICOS DOS TRÊS PARÂMETROS")
 print("*************************************************")
 # DADOS ESTATISTICOS
 print(DataFrame.describe())
     


# **********************************
# * SEPARAR OS CAMPOS PARA ANALISE *
# **********************************
hora=[]
batimento=[]
pressao=[]
temperatura=[]
for i in range(0,len(dados)):
    hora.append(dados[i]["HORA"])
    batimento.append(float(dados[i]["BATIMENTO"]))
    pressao.append(float(dados[i]["PRESSAO"]))
    temperatura.append(float(dados[i]["TEMPERATURA"]))

# PLOTAR DADOS
plt.plot( batimento, 'b')
plt.title("SINAL BATIMENTO CARDIACO")
plt.xlabel("AMOSTRA")
plt.ylabel("AMPLITUDE")
plt.show()

plt.plot( pressao, 'b')
plt.title("SINAL PRESSAO ARTERIAL")
plt.xlabel("AMOSTRA")
plt.ylabel("AMPLITUDE")
plt.show()

plt.plot( temperatura, 'b')
plt.title("SINAL TEMPERATURA")
plt.xlabel("AMOSTRA")
plt.ylabel("AMPLITUDE")
plt.show()


# *******************************************************************************
# EXEMPLO DE APLICACAO DE CORRELACAO PARA OS DADOS DE BATIMENTO CARDIACO
# *******************************************************************************
print("\n\nAPLICACAO DE CORRELACAO PARA OS DADOS DE BATIMENTO CARDIACO")
# SEPARAR O PRIMEIRO PACOTE DE BATIMENTO CARDIACO COMO PADRÃO BASE - 24 AMOSTRAS
Padrao=batimento[0:24]

# VETOR PARA ARMAZENAMENTO DOS DADOS - ANALISE DE BATIMENTOS CARDIACOS
Dados=[]
Dados=batimento


fator=int(len(Dados)/24)

LISTAPADRAO=[]
LISTAPADRAO.append(Padrao)

rDados=[]

BMedia=[]
for i in range(fator):
     rDados=Dados[i*24:(i+1)*24]

     # DEFINIR DataFrame COM OS VALORES LIDOS PARA APLICAR CORRELACAO
     auxDF=[]
     DataFrame=[]

     # z VARIAVEL AUXILIAR PARA MONTAGEM DO DATAFRAME
     auxDF+=[(float(float(Padrao[j])),float(rDados[j])) for j in range(0,len(Padrao))]

     # MONTAGEM
     DataFrame = pd.DataFrame(auxDF,columns=['PADRAO', 'RECORTE'])

  
     # CALCULAR A CORRELAÇÃO
     correlacao = DataFrame.corr(method='pearson')
     cp=correlacao["RECORTE"][0]
     print("\nCORRELAÇÃO TEMPORAL: ")
     print("PACOTE : ", i,"  [",i*24,": ",(i+1)*24,"]  NUMERO DE PADROES:",len(LISTAPADRAO))
     
     print(correlacao)
     print("\nDADOS ESTATISTICOS BÁSICOS - TEMPORAL: ")
     print("NUMERO DE AMOSTRAS/CAMPOS: ",DataFrame.shape)
     Estat=DataFrame.describe()
     # BATIMENTO MEDIO
     media=Estat["RECORTE"][1]
     BMedia.append(media)
     print(Estat)
     plt.plot( BMedia, 'b')
     plt.title("SINAL EVOLUCAO BATIMENTO MEDIO")
     plt.xlabel("AMOSTRA")
     plt.ylabel("AMPLITUDE")
     plt.show()
     
     if(cp<0.7):
         for vpd in range(len(LISTAPADRAO)):
             print("COMPARANDO O PACOTE ",i, " COM O PADRAO: ",vpd," - ",LPD[vpd])
             rPDaux=LISTAPADRAO[vpd]
             # DEFINIR DataFrame COM OS VALORES LIDOS PARA APLICAR CORRELACAO
             auxDF2=[]
             DataFrame2=[]

             # z VARIAVEL AUXILIAR PARA MONTAGEM DO DATAFRAME
             auxDF2+=[(float(float(rPDaux[v])),float(rDados[v])) for v in range(0,len(rDados))]
        
             # MONTAGEM
             DataFrame = pd.DataFrame(auxDF2,columns=['rPADRAO', 'RECORTE'])
  
             # CALCULAR A CORRELAÇÃO
             correlacao = DataFrame.corr(method='pearson')
             cp=correlacao["RECORTE"][0] 
             print("CORRELACAO = ",cp)
 
         T=input("DESEJA ARMAZENAR ESTE RECORTE: <S/N>")
         if (T=="S" or T=="s"):
            #ARMAZENAR EM UMA LISTA
            LISTAPADRAO.append(rDados)
            textodopadrao=input("DIGITAR CODIGO DO ERRO: ")
            LPD.append(textodopadrao) 
 

     t=input("DIGITE ALGO:") 

plt.plot( BMedia, 'b')
plt.title("SINAL EVOLUCAO BATIMENTO MEDIO")
plt.xlabel("AMOSTRA")
plt.ylabel("AMPLITUDE")
plt.show()