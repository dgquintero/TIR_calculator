#!/usr/bin/env python3
from datetime import datetime
import pandas as pd
import numpy as np
import csv

# cargar los datos del csv a arrays
indicadores = []
dividendos = []
with open("indicadores.csv") as csvfile:
    reader = csv.reader(csvfile) 
    for row in reader: # each row is a list
        indicadores.append(row)

with open("dividendos.csv") as csvfile_div:
    reader_div = csv.reader(csvfile_div) 
    for div in reader_div: # each row is a list
        dividendos.append(div)

tabla = [['12/6/15', 'retiro', 12, 1.4],
         ['12/7/15', 'inversion', 20, 10.9],
         ['12/12/15', 'retiro', 20, 10.9],
         ['12/1/17', 'inversion', 100, 10.9],]

def calc_tir():
    """
    Los datos de entrada de la aplicación son:
        - Fecha de la consulta
        - Transacciones de compra y venta con: Fecha, Número de acciones y valor
    """
    flujo = []


    # Consultas
    #ask_date = input("Por favor escriba el día de consulta (AAAA-MM-DD): ")
    #transaction = input("Por favor escriba el tipo de transaccion que desea realizar (inversion o retiro): ")

    array_indi = []
    for j in range(1, len(indicadores)):
        time_obj = datetime.strptime(indicadores[j][1], '%m/%d/%y')
        array_indi.append([time_obj.date(), float(indicadores[j][2])])

    array_divi = []
    for j in range(1, len(dividendos)):
        time_obj = datetime.strptime(dividendos[j][1], '%m/%d/%y')
        array_divi.append([time_obj.date(), float(dividendos[j][2])])

    for j in range(len(tabla)):
        time_obj = datetime.strptime(tabla[j][0], '%m/%d/%y')
        tabla[j][0] = time_obj.date()

    array_acciones = []
    acciones = 0
    # calculo del flujo si es inversión o retiro
    for i in range(len(tabla)):
        if tabla[i][1] == 'inversion':
            flujo.append(tabla[i][2] * tabla[i][3])
            acciones += tabla[i][2]
            array_acciones.append([tabla[i][0], acciones])
        elif tabla[i][1] == 'retiro':
            flujo.append(-(tabla[i][2] * tabla[i][3]))
            acciones -= tabla[i][2]
            array_acciones.append([tabla[i][0], acciones])
        for b in range(len(array_divi)):
            print(tabla[i][0] >= array_divi[b][0])

            if tabla[i][0] >= array_divi[b][0] and array_divi[b][0] < tabla[i + 1][0]:
                flujo.append(round(float(array_acciones[i][1] * array_divi[b][1]), 5))
    

    # Calculo salida acciones

    print(flujo)

    # calculo tir con flujos
    print (round(np.irr(flujo), 5))

calc_tir()
