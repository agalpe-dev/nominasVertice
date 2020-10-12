import PyPDF2
import re
import sys
import os.path

def getArchivoLibre (txt):
    while os.path.isfile(txt):
        nombre = txt.split('.')[0]
        ext = txt.split('.')[1]
        x = nombre[-1]
        if x.isnumeric():
            x = int(x) + 1
            txt = nombre[0:-1] + str(x) + "." + ext
        else:
            nombre = nombre + "_1"
            txt = nombre + "." + ext
    return txt

def existeEntrada(entrada):
	try:
		f=open(entrada, 'r')
	except Exception as e:
		print("Archivo de entrada no encontrado")
		return False
	f.close()
	return True

def guardatxt(texto, archivo):
	output=archivo+".txt"
	try:
	    f=open(output,'w')
	    f.write(texto)
	    f.close()
	except Exception as e:
	    print("Error al guardar el archivo de texto.")

def getNombre(texto):
	lineas=texto.split("\n")
	linea=lineas[-1]
	if linea=="":
		linea=lineas[-2]
	nombre = linea[46:86]
	nombre = nombre.strip()
	nombre2 = ""
	for letra in nombre:
			if letra != ".":
				nombre2 = nombre2 + letra
	nombre = nombre2.strip()
	return nombre

def getYear(texto):
	lineas = texto.split("\n")
	linea = lineas[-1]
	if linea == "":
		linea = lineas[-2]
	year = linea[458:462]
	year = year.strip()
	return year

def getMes(texto):
	lineas=texto.split("\n")
	linea=lineas[-1]
	if linea=="":
		linea=lineas[-2]
	mes = linea[424:439]
	mes = mes.strip()
	mes = mes.lower()
	meses={"enero": "01", "febrero": "02", "marzo": "03", "abril": "04", 
	"mayo": "05", "junio": "06", "julio": "07", "agosto": "08", "septiembre": "09",
	"octubre": "10", "noviembre": "11", "diciembre": "12"}
	mesn=meses[mes]
	return mesn

# comprueba que se le pasa algun argumento en la linea de comandos
if len(sys.argv) != 2:
	print("*** Vértice - Separador de nóminas *** (by Antonio)")
	print("uso: pdf2.py archivo_de_nominas.pdf\n")
	sys.exit()
else:
	# se comprueba si el argumento es un archivo existente, si no lo es, finaliza el programa
	entrada=sys.argv[1]
	if existeEntrada(entrada) == False:
		sys.exit()


# entrada = "archivo.pdf" --> solo para pruebas
# abro el archivo dado en la linea de argumentos
pdfObj = open(entrada, 'rb')

# Objeto reader
pdfReader = PyPDF2.PdfFileReader(pdfObj)


# diccionario con las equivalencias de cif y empresa
empresas = {"B92972124" : "CV1979", "B11305000" : "MCL", "B98138274" : "VFE"}

# comprobar si el archivo está encriptado
if pdfReader.isEncrypted:
	print ("documento encriptado: No se puede extraer el texto hasta desencriptarlo")	    
else:
    # iteración por cada pagina del archivo pdf
   	for page in range(pdfReader.numPages):
	    #objeto pdfWriter
	    pdfWriter=PyPDF2.PdfFileWriter()
	    print("Trabajando... Pág %d de %d" % (page.numerator+1,pdfReader.numPages))
	    pagina=pdfReader.getPage(page)
	    texto=pagina.extractText()

	    #se intenta comprimir cada pagina
	    pagina.compressContentStreams()
		
	    # busco dni, cif y si aparece la palabra finiquito mediante regex
	    dni=re.search('\d{8}[A-Z]', texto)
	    cif=re.search('B\d{8}', texto)
	    finiquito=re.findall("FINIQUITO",texto)

	    # busco en el diccionario empresas el nombre que corresponde con el cif encontrado
	    empresa=empresas[cif.group()]
		
	    # si existe la palabra finiquito se le añade al nombre del archivo de salida
	    if len(finiquito) > 0:
		    nombreSalida=getYear(texto)+"-"+getMes(texto)+"_"+empresa+"_"+getNombre(texto)+"_"+dni.group()+"_FINIQUITO.pdf"
	    else:
		    nombreSalida=getYear(texto)+"-"+getMes(texto)+"_"+empresa+"_"+getNombre(texto)+"_"+dni.group()+".pdf"
			
	    # crea un archivo txt con el texto de cada pagina (Para pruebas)
	    # guardatxt(texto, getNombre(texto))
		
	    # TODO: mejorar creando una funcion para esto que compruebe si ya existe el archivo y no lo sobreescriba
	    # archivo=open(nombreSalida, 'wb')
	    nombreArchivo = getArchivoLibre(nombreSalida)
	    archivo = open(nombreArchivo, 'wb')
		
	    pdfWriter.addPage(pagina)
	    pdfWriter.write(archivo)
			
	    	

print("Proceso finalizado!")
pdfObj.close()
archivo.close()
