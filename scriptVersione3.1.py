#Librerie utilizzate
import os, time, csv

oldLines = 0														
lastEditTxt = os.stat("temperature.txt").st_mtime					
while True:
	newEditTxt = os.stat("temperature.txt").st_mtime
	#se oldLines è uguale o maggiore a 3600 (1h) si crea il file di backup
	#e si elimina il contenuto di temperature.txt
	if oldLines >= 3600:
		#DA IMPLEMENTARE
	if newEditTxt > lastEditTxt:
		fileTxt = open("temperature.txt", "r")
		data = fileTxt.readlines()
		newLines = len(data)
		while oldLines < newLines - 1:
			riga = data[oldLines]
			riga.replace("\n", "")
			lista = riga.split("   ")
			
			oldLines = oldLines + 1
		lastEditTxt = newEditTxt
		fileTxt.close()
		time.sleep(5)

		
'''	
    Legenda:
	oldLines = numero delle righe lette fino ad ora;
	lastEditTxt = vecchia data dell'ultima modifica del file creato dal minicom;
	newEditTxt	= nuova data dell'ultima modifica del file creato dal minicom;
	data = lista di stringhe. Contiene tutto il contenuto del file fileTxt;
	newLines = numero delle righe lette fino ad ora (aggiornate);
'''