import pandas as pd
import numpy as np
import statistics as st


Synergy=pd.read_csv(r'C:\Users\LENOVO\Documents\synergy_logistics_database.csv')

Synergy["Ruta"] = Synergy["origin"].map(str) + '-' + Synergy["destination"].map(str) 

#Total porcentual dividido entre exportaciones e importanciones por ruta. 

Rutas_Exportaciones =Synergy[Synergy.direction == "Exports"]
Rutas_Importaciones =Synergy[Synergy.direction == "Imports"]

#Exportaciones

Mayores_Rutas_Exp=Rutas_Exportaciones['Ruta'].value_counts(ascending=False).to_frame()
Mayores_Rutas_Exp= Mayores_Rutas_Exp.rename(columns={'Ruta': '# de exportaciones'})
Mayores_Rutas_Exp.index.name = 'Ruta'
Mayores_Rutas_Exp.reset_index(inplace=True)
print(f'El mayor número de exportaciones ocurre en las siguientes rutas:')
print(f'{Mayores_Rutas_Exp.head(n=10).to_string(index=True)}')

Mayores_Rutas_Exp_Porcentajes=Rutas_Exportaciones['Ruta'].value_counts(ascending=False,normalize=True).to_frame()
Mayores_Rutas_Exp_Porcentajes= Mayores_Rutas_Exp_Porcentajes.rename(columns={'Ruta': '% de exportaciones'})
Mayores_Rutas_Exp_Porcentajes.index.name = 'Ruta'
Mayores_Rutas_Exp_Porcentajes.reset_index(inplace=True)
Mayores_Rutas_Exp_Porcentajes["% de exportaciones"] = round(100 * Mayores_Rutas_Exp_Porcentajes["% de exportaciones"],2)
print(f'El mayor % del total de exportaciones ocurre en las siguientes rutas:')
print(f'{Mayores_Rutas_Exp_Porcentajes.head(n=10).to_string(index=True)}')

#Importaciones

Mayores_Rutas_Imp=Rutas_Importaciones['Ruta'].value_counts(ascending=False).to_frame()
Mayores_Rutas_Imp= Mayores_Rutas_Imp.rename(columns={'Ruta': '# de importaciones'})
Mayores_Rutas_Imp.index.name = 'Ruta'
Mayores_Rutas_Imp.reset_index(inplace=True)
print(f'El mayor número de importaciones ocurre en las siguientes rutas:')
print(f'{Mayores_Rutas_Imp.head(n=10).to_string(index=True)}')

Mayores_Rutas_Imp_Porcentajes=Mayores_Rutas_Imp['Ruta'].value_counts(ascending=False,normalize=True).to_frame()
Mayores_Rutas_Imp_Porcentajes= Mayores_Rutas_Imp_Porcentajes.rename(columns={'Ruta': '% de exportaciones'})
Mayores_Rutas_Imp_Porcentajes.index.name = 'Ruta'
Mayores_Rutas_Imp_Porcentajes.reset_index(inplace=True)
Mayores_Rutas_Imp_Porcentajes["% de exportaciones"] = round(100 * Mayores_Rutas_Imp_Porcentajes["% de exportaciones"],2)
print(f'El mayor % del total de exportaciones ocurre en las siguientes rutas:')
print(f'{Mayores_Rutas_Imp_Porcentajes.head(n=10).to_string(index=True)}')

column_number = 2
Total_top_Exp = Mayores_Rutas_Exp_Porcentajes.iloc[0:9, column_number-1:column_number].sum()
print(f'El total del top 10 de exportaciones es: {round(Total_top_Exp[0],2)} % de ellas')
print(f'Por lo tanto, no sería buena idea tomar unicamente el top 10 de exportaciones e importanciones, al igual que tomar 5 mayores exportaciones o 5 mayores exportaciones: ')


#Veamos ahora el total porcentual por ruta para tomar el top 5 y top 5 de exportaciones e importaciones.  

Top_total_Rutas=Synergy.groupby(['direction'])['Ruta'].value_counts(ascending=False).to_frame()
Top_total_Rutas= Top_total_Rutas.rename(columns={'Ruta': 'Veces_Demandado'})
Top_total_Rutas.index.name = 'Ruta'
Top_total_Rutas.reset_index(inplace=True)
Top_total_Rutas["Demanda (%)"] = (Top_total_Rutas['Veces_Demandado'] / Top_total_Rutas['Veces_Demandado'].sum()) * 100
Top_total_Rutas_2=Synergy.groupby(['direction','Ruta'])['total_value'].sum().to_frame()
Top_total_Rutas_2= Top_total_Rutas_2.rename(columns={'total_value': 'Valor total'})
Top_total_Rutas_2.index.name = 'Ruta'
Top_total_Rutas_2.reset_index(inplace=True)
Top_total_Rutas_2["Valor total (%)"] = (Top_total_Rutas_2['Valor total'] / Top_total_Rutas_2['Valor total'].sum()) * 100
Base_completa = pd.merge(Top_total_Rutas, Top_total_Rutas_2, how='left', on=None, left_on=None, right_on=None,
         left_index=True, right_index=True, sort=True)

Base_completa = Base_completa.rename(columns={'direction_x': 'direction'})
Base_completa = Base_completa.rename(columns={'Ruta_x': 'Ruta'})
Base_completa=Base_completa.drop(labels=['direction_y', 'Ruta_y'], axis=1)
Base_completa=Base_completa.sort_values(["Valor total"], ascending=False)


Total_top_Porcentaje_Exp=Top_total_Rutas[Top_total_Rutas.direction == "Exports"]
Total_top_Porcentaje_Imp=Top_total_Rutas[Top_total_Rutas.direction == "Imports"]
column_number = 4
Total_top_Porcentaje_Exp = Total_top_Porcentaje_Exp.iloc[0:10, column_number-1:column_number].sum()
print(f'La suma porcentual del top 10 de exportaciones es: {round(Total_top_Porcentaje_Exp[0],2)} % de ellas')
column_number = 4
Total_top_Porcentaje_Imp = Total_top_Porcentaje_Imp.iloc[0:10, column_number-1:column_number].sum()
print(f'La suma porcentual del top 10 de importaciones es: {round(Total_top_Porcentaje_Imp[0],2)} % de ellas')
print(f'Al sumar ambas, encontramos poco más del 27 % del total de las exportaciones de Synergy, se concluye que no es una buena idea, quedarse con únicamente las 10 rutas más demandadas. Por lo menos deberín ser el 70% del total. Además, observamos que en cuestión de valor total, aunque sean las rutas más demandadas, muchas de ellas, no representan un buen porcentaje del valor total')

#Por el valor

Total_top_Porcentaje_Exp=Base_completa[Base_completa.direction == "Exports"]
Total_top_Porcentaje_Imp=Base_completa[Base_completa.direction == "Imports"]

column_number = 6
Total_top_Porcentaje_Exp = Total_top_Porcentaje_Exp.iloc[0:10, column_number-1:column_number].sum()
print(f'La suma porcentual del top 10 de exportaciones es: {round(Total_top_Porcentaje_Exp[0],2)} % de ellas')
column_number = 6
Total_top_Porcentaje_Imp = Total_top_Porcentaje_Imp.iloc[0:10, column_number-1:column_number].sum()
print(f'La suma porcentual del top 10 de importaciones es: {round(Total_top_Porcentaje_Imp[0],2)} % de ellas')
print(f'Al sumar ambas, encontramos poco más del 16 % del total de las exportaciones de Synergy, se concluye que no es una buena idea, quedarse con únicamente las 10 rutas más demandadas. Por lo menos deberín ser el 70% del total. Además, observamos que en cuestión de valor total, aunque sean las rutas más demandadas, muchas de ellas, no representan un buen porcentaje del valor total')

#Observemos cual es el porcentaje total de demanda que tienen los productos de importacion y los de exportación

Top_total_Direccion=Synergy['direction'].value_counts(ascending=False).to_frame()
Top_total_Direccion= Top_total_Direccion.rename(columns={'direction': 'Veces_Demandado'})
Top_total_Direccion.index.name = 'direction'
Top_total_Direccion.reset_index(inplace=True)
Top_total_Direccion["%"] = (Top_total_Direccion['Veces_Demandado'] / Top_total_Direccion['Veces_Demandado'].sum()) * 100
Total_top_Porcentajes= Top_total_Direccion.loc[:1,["%"]]
column_number = 1
Total_top_Porcentajes = Total_top_Porcentajes.iloc[0:1,].sum()
print(f'La cantidad de exportaciones tiene mucha mayor demanda que las importaciones, representando el {round(Total_top_Porcentajes[0],2)} % del total de todos los productos que transporta Synergy')

#Medios de transporte más utilizados por el valor de las exportaciones e importaciones

Medios_de_transporte=Synergy.groupby(['direction','transport_mode'])['total_value'].sum().to_frame()
Medios_de_transporte = Medios_de_transporte.sort_values(by = ['direction', 'total_value'], ascending=[True,False])
Medios_de_transporte.reset_index(inplace=True)
Medios_de_transporte_Exp = Medios_de_transporte[Medios_de_transporte.direction == "Exports"]
#Medios_de_transporte_Exp =Medios_de_transporte_Exp ['transport_mode'].tolist()
Medios_de_transporte_Imp = Medios_de_transporte[Medios_de_transporte.direction == "Imports"]
#Medios_de_transporte_Imp =Medios_de_transporte_Imp['transport_mode'].tolist()

#Medios_de_transporte_Val_Exp = Medios_de_transporte[Medios_de_transporte.direction == "Exports"]
#Medios_de_transporte_Val_Exp = Medios_de_transporte_Val_Exp['total_value'].tolist()
#Medios_de_transporte_Val_Imp = Medios_de_transporte[Medios_de_transporte.direction == "Exports"]
#Medios_de_transporte_Val_Imp = Medios_de_transporte_Val_Imp['total_value'].tolist()

Medios_de_transporte_Exp_3Prim = Medios_de_transporte_Exp.head(3)
Medios_de_transporte_Exp_3Prim=Medios_de_transporte_Exp_3Prim.drop(labels=['direction'], axis=1)

print(f'En el caso de las exportaciones, tenemos los siguientes 3 medios de transporte:')
print(Medios_de_transporte_Exp_3Prim)

Medios_de_transporte_Imp_3Prim = Medios_de_transporte_Imp.head(3)
Medios_de_transporte_Imp_3Prim=Medios_de_transporte_Imp_3Prim.drop(labels=['direction'], axis=1)

print(f'En el caso de las importaciones, tenemos los siguientes 3 medios de transporte:')
print(Medios_de_transporte_Imp_3Prim)

print(f'Si tuvieramos que elegir de las dos 3 medios de transporte, elegiriamos los siguientes:')

Medios_de_transporte_total=Synergy.groupby(['transport_mode'])['total_value'].sum().to_frame()
Medios_de_transporte_total = Medios_de_transporte_total.sort_values(by = 'total_value', ascending=False)
Medios_de_transporte_total_3Prim = Medios_de_transporte_total.head(3)

print(Medios_de_transporte_total_3Prim) 
print(f'Que es la suma del valor total por transporte. Pudiendo reducir por lo tanto, el medio de transporte road')

#80% del valor de exportaciones e importaciones

Paises=Synergy.groupby(['origin'])['total_value'].sum().to_frame()
Paises= Paises.rename(columns={'total_value': 'Valor total'})
Paises.index.name = 'País'
Paises.reset_index(inplace=True)
Paises["Valor total (%)"] = (Paises['Valor total'] / Paises['Valor total'].sum()) * 100
Paises = Paises.sort_values(by ='Valor total (%)', ascending=False)
Paises["% acumulado"] = Paises["Valor total (%)"].cumsum()
top_80=Paises[Paises["% acumulado"]<82]