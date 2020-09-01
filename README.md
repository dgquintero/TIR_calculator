# TIR_calculator app

La TIR puede utilizarse como indicador de la rentabilidad de un proyecto: a mayor TIR, mayor rentabilidad. 

Esta calculadora te permite calcular la TIR basada en el flujo de caja, inversiones y retiros, en acciones de una compañía. Los flujos incluyen los dividendos generados por las acciones entre los periodos. 

Para completar el formulario debes tener a la mano fecha de las inversiones  o retiros, el número de acciones en cada transacción y el precio de la acción para cada día. 

Fecha de Consulta 
Fecha Transacción, Número de Acciones, Valor de la Acción y Tipo Transacción  


Ejericio de realizar una calculadora de TIR (Tasa interna de retorno)

````
pip install numpy
pip install pandas
pip install flask
````

Para probar el ejercicio se requiere tener instalado las anteriores dependencias y en la dirección del repositorio correr el archivo app.py

````
flask run
````

## Bugs

- En el momento está hecha para recibir 4 transacciones obligatoriamente, se tienen que implemanr n transacciones.

- Las casillas permiten cualquier clase de input lo que para una mejora se tienen que implementar casillas con verificación que impidan el error humano.

- Para el calculo de la TIR está colocando en desorden los flujos lo que influye circunstancialmente en el resultado.
