# nominas.py

Script para la división de archivos pdf de nóminas con varios trabajadores, empresas o periodos en archivos individuales por trabajador.
Es una herramienta útil para el departamento de RR.HH. que recibe o tiene un único documento pdf con las nóminas de todos los trabajadores ya que automatiza separar la nómina de cada trabajador creando un archivo individual por nómina.

El nombre de los archivos resultantes siguen el esquema año-mes_empresa_Nombre_DNI.pdf. Eventualmente, se añade "_FINIQUITO" al final del nombre si es el caso.
Para el nombre de la empresa hace uso de un diccionario "empresas" con la estructura: "CIF":"Empresa" por lo que si se desea usar nuevas empresas habría que modificar este diccionario.
Si existe más de una nómina para un trabajador y un mismo periodo se generarán archivos diferentes diferenciándolos al final del mismo por un número "-1", "-2", etc...

El script es funcional con los archivos pdf generados por el programa de nóminas Monitor. No se ha probado con archivos generados con otros programas de nóminas.
