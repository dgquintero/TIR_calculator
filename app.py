#!/usr/bin/env python3
from datetime import datetime
import pandas as pd
import numpy as np
import csv
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('app.html')

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

# tabla con los valores que van a hacer recogidos por l pagina
tabla = [['12/6/15', 'retiro', 12, 1.4],
         ['12/7/15', 'inversion', 20, 10.9],
         ['12/12/15', 'retiro', 20, 10.9],
         ['12/1/17', 'inversion', 100, 10.9]]

# dato que va a entrar por consulta que es la fecha de consulta
consulta = datetime.strptime('8/30/20', '%m/%d/%y')
consulta = consulta.date()

@app.route('/send', methods=['POST'])
def calc_tir():
    """
    Los datos de entrada de la aplicación son:
        - Fecha de la consulta
        - Transacciones de compra y venta con: Fecha, Número de acciones y valor
    """
    if request.method == 'POST':
        consulta = request.form['dia_con']
        fecha_ing = request.form['fecha_ing']
        numero_ac = request.form['numero_ac']
        valor_ac = request.form['valor_ac']
        operacion = request.form['operacion']
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
    for i in range(len(tabla) - 1):
        if tabla[i][1] == 'inversion':
            flujo.append(tabla[i][2] * tabla[i][3])
            acciones += tabla[i][2]
            array_acciones.append([tabla[i][0], acciones])
        elif tabla[i][1] == 'retiro':
            flujo.append(-(tabla[i][2] * tabla[i][3]))
            acciones -= tabla[i][2]
            array_acciones.append([tabla[i][0], acciones])

        # calcular dividendos en las fechas especificas
        for b in range(len(array_divi)):
            print(tabla[i][0] <= array_divi[b][0] and array_divi[b][0] > tabla[i + 1][0])
            if tabla[i][0] <= array_divi[b][0] and array_divi[b][0] > tabla[i + 1][0]:
                flujo.append(round(float(array_acciones[i][1] * array_divi[b][1]), 5))
                    
        if (i + 1) == len(tabla):
            exit

    # Calculo salida acciones
    for i in range(1, len(array_indi)):
        if consulta == array_indi[i][0]:
            flujo.append(-(array_indi[i][1] * acciones))


    print(flujo)

    # calculo tir con flujos
    return (round(np.irr(flujo), 5))

if __name__ == ' __main__':
    app.debug = True
    app.run()
