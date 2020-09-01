from datetime import datetime
import pandas as pd
import numpy as np
import csv

from flask import Flask, render_template, request

app = Flask(__name__)


# cargar los datos de los archivos dados
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

@app.route('/')
def main():
    return render_template("app.html")


@app.route("/send", methods=['POST'])
def calculate():
    consulta = datetime.strptime(request.form['dia_con'], '%m/%d/%y')
    consulta = consulta.date()

    tabla = []
    arra1 = []
    if request.method == 'POST':
        try:
            arra1.append(request.form['fecha_ing1'])
            arra1.append(int(request.form['numero_ac1']))
            arra1.append(int(request.form['valor_ac1']))
            arra1.append(request.form['operacion1'])

            tabla.append(arra1)
            arra1 = []

            arra1.append(request.form['fecha_ing2'])
            arra1.append(int(request.form['numero_ac2']))
            arra1.append(int(request.form['valor_ac2']))
            arra1.append(request.form['operacion2'])
            tabla.append(arra1)
            arra1 = []

            arra1.append(request.form['fecha_ing3'])
            arra1.append(int(request.form['numero_ac3']))
            arra1.append(int(request.form['valor_ac3']))
            arra1.append(request.form['operacion3'])
            tabla.append(arra1)
            arra1 = []

            arra1.append(request.form['fecha_ing4'])
            arra1.append(int(request.form['numero_ac4']))
            arra1.append(int(request.form['valor_ac4']))
            arra1.append(request.form['operacion4'])
            tabla.append(arra1)

            #dates preprocesamiento
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

            flujo = []
            array_acciones = []
            acciones = 0
            # calculo del flujo si es inversión o retiro
            for i in range(len(tabla)):
                if tabla[i][3] == 'inversion':
                    flujo.append(tabla[i][1] * tabla[i][2])
                    acciones += tabla[i][1]
                    array_acciones.append([tabla[i][0], acciones])
                elif tabla[i][3] == 'retiro':
                    flujo.append(-1 * (tabla[i][1] * tabla[i][2]))
                    acciones -= tabla[i][1]
                    array_acciones.append([tabla[i][0], acciones])
            
            
            # calcular dividendos en las fechas especificas
            for i in range(len(array_acciones) - 1):
                for b in range(len(array_divi)):
                    if array_acciones[i][0] <= array_divi[b][0] and array_divi[b][0] > array_acciones[i + 1][0]:
                        flujo.insert(i + 1, round(float(array_acciones[i][1] * array_divi[b][1]), 5))
            
            # Calculo salida acciones
            for i in range(1, len(array_indi)):
                if consulta == array_indi[i][0]:
                    flujo.append(round(-(array_indi[i][1] * acciones), 2))
            

            # calculo tir con flujos
            tir = round(np.irr(flujo), 5)

            return render_template('app.html', result=tir)
        except:
            return render_template('app.html')
            #return

    #else:
    #    return render_template('app.html')

if __name__ == '__main__':
    app.run(debug = True)
