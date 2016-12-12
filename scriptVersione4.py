	#Librerie utilizzate
import os, csv, time
from time import gmtime, strftime
#campiJSON = { "id", "utc_timestamp", "lat", "lon", "ele", "temp", "angle1", "angle2"}
campiJSON = { "id", "utc_timestamp"}
oldLines = 0														
lastEditTxt = os.stat("temperature.txt").st_mtime					
while True:
	newEditTxt = os.stat("temperature.txt").st_mtime
	
	
	if newEditTxt > lastEditTxt:
		fileTxt = open("temperature.txt", "r")
		fileBackup = open(strftime("%Y-%m-%d-%H:00.json", gmtime()),"a")
		data = fileTxt.readlines()
		newLines = len(data)
		while oldLines < newLines - 1:
			riga = data[oldLines]
			riga.replace("\n", "")
			lista = riga.split("   ")
			oggettoJSON = "{ "
			i = 0
			for campo in campiJSON:
				oggettoJSON = oggettoJSON + "\"" + campo + "\": \"" + lista[i] + "\","
				i = i + 1
			oggettoJSON = oggettoJSON[:-1]
			oggettoJSON = oggettoJSON + " },"
			fileBackup.write(oggettoJSON)
			oldLines = oldLines + 1
		lastEditTxt = newEditTxt
		fileTxt.close()
		time.sleep(5)

		
'''	Legenda:
	oldLines = numero delle righe lette fino ad ora;
	lastEditTxt = vecchia data dell'ultima modifica del file creato dal minicom;
	newEditTxt	= nuova data dell'ultima modifica del file creato dal minicom;
	data = lista di stringhe. Contiene tutto il contenuto del file fileTxt;
	newLines = numero delle righe lette fino ad ora (aggiornate); 
	Formato JSON -> { "timeStamp": 0.223123} 
'''