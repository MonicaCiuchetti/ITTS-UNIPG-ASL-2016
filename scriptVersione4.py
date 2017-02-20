	#Librerie utilizzate
import os, csv, time
from time import gmtime, strftime
from datetime import datetime
#campiJSON = { "id", "utc_timestamp", "lat", "lon", "ele", "temp", "angle1", "angle2"}
campiJSON = { "id", "utc_timestamp"}
oldLines = 0														
lastEditTxt = os.stat("temperature.txt").st_mtime
giorno = datetime.now().day
ora = datetime.now().hour
path = os.environ('HOME') + "/" + strftime("%Y-%m-%d",gmtime())
os.mkdir(path)
virgola = False

schema = avro.schema.parse(open("schema-prova.avsc", "rb").read())
					
while True:
	newEditTxt = os.stat("temperature.txt").st_mtime
	if giorno != datetime.now().day:
		giorno = datetime.now().day
		path = os.environ('HOME') + "/" + strftime("%Y-%m-%d",gmtime())
		os.mkdir(path)
	if ora != datetime.now().hour:
		virgola = False
		ora = datetime.now().hour
	fileBackup = open(strftime(path + "/%Y-%m-%d-%H:00.json", gmtime()),"a")
	writer = DataFileWriter(open(strftime(path + "/%Y-%m-%d-%H:00.avro", gmtime()), "ab"), DatumWriter(), schema)
	if newEditTxt > lastEditTxt:
		fileTxt = open("temperature.txt", "r")
		data = fileTxt.readlines()
		newLines = len(data)
		while oldLines < newLines - 1:
			riga = data[oldLines]
			riga.replace("\n", "")
			lista = riga.split("   ")
			if virgola:
				fileBackup.write(",")
			else:
				virgola = True
			oggettoJSON = "{ "
			i = 0
			for campo in campiJSON:
				oggettoJSON = oggettoJSON + "\"" + campo + "\": \"" + str(lista[i]).replace("\n", "") + "\","
				i = i + 1
			oggettoJSON = oggettoJSON[:-1]
			oggettoJSON = oggettoJSON + " }"
			fileBackup.write(oggettoJSON)
			writer.append(json.loads(oggettoJSON))
			oldLines = oldLines + 1
		lastEditTxt = newEditTxt
		fileTxt.close()
		fileBackup.close()
		writer.close()
		time.sleep(5)

		
'''	Legenda:
	oldLines = numero delle righe lette fino ad ora;
	lastEditTxt = vecchia data dell'ultima modifica del file creato dal minicom;
	newEditTxt	= nuova data dell'ultima modifica del file creato dal minicom;
	data = lista di stringhe. Contiene tutto il contenuto del file fileTxt;
	newLines = numero delle righe lette fino ad ora (aggiornate); 
	Formato JSON -> { "timeStamp": 0.223123} 
'''
