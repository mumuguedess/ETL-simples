# link dos dados de colheita https://www.kaggle.com/datasets/thedevastator/the-relationship-between-crop-production-and-cli/
# link dos dados de temperatura: https://www.kaggle.com/datasets/jawadawan/global-warming-trends-1961-2022/data?select=long_format_annual_surface_temp.csv


import pandas as pd 

#Extração dos dados para análise
dados_colheita = pd.read_csv("crop_production.csv")
dados_temperatura = pd.read_csv("long_format_annual_surface_temp.csv")

#Remoção das localidades OECD, BRICS e EU28
dados_colheita = dados_colheita.loc[~dados_colheita['LOCATION'].isin(["OECD", "BRICS", "EU28"])]

#Adição do código de 3 letras para cada país nos dados de temperatura
country_codes = pd.read_csv("country_codes.csv")
country_codes = country_codes[["Alpha-2 code", "Alpha-3 code"]]
country_codes = country_codes.rename(columns={"Alpha-2 code" : "ISO2", "Alpha-3 code" : "LOCATION"})
dados_temperatura = pd.merge(dados_temperatura, country_codes, on="ISO2")

#Mescla dos dados baseado no país e ano
dados_temperatura = dados_temperatura.rename(columns={"Year" : "TIME"})
dados_temperatura["TIME"] = dados_temperatura["TIME"].str.slice(1)
dados_temperatura["TIME"] = dados_temperatura["TIME"].astype(int)
resultado = pd.merge(dados_colheita, dados_temperatura, on=["TIME", "LOCATION"])

#Remoção de colunas que não me fornecem muita informação
resultado = resultado.drop(columns=["INDICATOR", "FREQUENCY", "Flag Codes", "ISO2", "Country", "index"])

#Carregamento em um csv
resultado.to_csv("Resultado.csv", index=False)

