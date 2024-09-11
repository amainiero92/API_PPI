import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
#from pandas_datareader import data as pdr


stack= yf.Ticker("AAPL")
stack.dividends #Dividendos

stack.dividends.plot(kind='bar') #Grafico

stack.financials #Datos financieros

stack_df=stack.financials.T #cambio de nombre a mas corto
stack_df.columns #Detalle de datos que puedo traer por separado
stack_df['Net Income'] #Elijo traer solo alguno de esos datos

#Trabajo con iteracion de datos y listas
list_tickers=("AAPL","MSFT","NVDA","AMZN","GOOGL") 
net_income_list=[]
for ti in list_tickers[0:5]:
        stack_df=yf.Ticker(ti)
        stack_df=stack_df=stack.financials.T['Net Income']
        net_income_list.append(stack_df.rename(ti))
net_income_list #llamo a la funcion

net_income_df=pd.concat(net_income_list,axis=1) #La ordeno en formato de columnas
net_income_df #llamo a la funcion

net_income_df.plot(kind="bar")










