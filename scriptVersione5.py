import os, time
from time import localtime, strftime
from datetime import datetime
import json

import avro.schema
from avro.io import DatumWriter

#Parametri
TIME_LOG = "minuto"
TIME_DIR = "ora"
AVRO_SCHEMA = "schema-prova.avsc"
LOG_PATH = "/home/asl-2016"

#Funzioni
def pickMinute():
	return datetime.now().minute

def pickHour():
	return datetime.now().hour

def pickDay():
	return datetime.now().day

def scriviFile(oldLines, fileBackup, virgola, campiJSON):
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
			oggettoJSON = oggettoJSON + "\"" + campo['name'] + "\": \"" + str(lista[i]).replace("\n", "") + "\","
			i = i + 1
		oggettoJSON = oggettoJSON[:-1]
		oggettoJSON = oggettoJSON + " }"
		fileBackup.write(oggettoJSON)
		oldLines = oldLines + 1
	lastEditTxt = newEditTxt
	fileTxt.close()
	time.sleep(5)

	return oldLines

#TIME_LOG - parametro per tempo di cambio file
#TIME_DIR - parametro per tempo di cambio cartella

if TIME_LOG == "minuto":
	TIME_LOG = pickMinute
	strTimeLog = "%Y-%m-%d-%H:%M.json"
elif TIME_LOG == "ora":
	TIME_LOG = pickHour
	strTimeLog = "%Y-%m-%d-%H:00.json"
else:
	raise ValueError

if TIME_DIR == "ora":
	TIME_DIR = pickHour
	strTimeDir = strTimeLog = "%Y-%m-%d-%H:00"
elif TIME_DIR == "giorno":
	TIME_DIR = pickDay
	strTimeDir = strTimeLog = "%Y-%m-%d"
else:
	raise ValueError

temp = open(AVRO_SCHEMA, "r")
campiJSON = json.loads(temp.read())['fields']
temp.close()

#Ultima modifica di inizializzazione
oldLines = 0
lastEditTxt = os.stat("temperature.txt").st_mtime

timeLog = TIME_LOG
timeDir = TIME_DIR
PATH = LOG_PATH + "/" + strTimeDir
os.mkdir(strftime(PATH, localtime()))
virgola = False

schema = avro.schema.parse(open("schema-prova.avsc", "rb").read())

while True:
	while timeDir is TIME_DIR:
		#DA PROVARE
		fileBackup = open(strftime(PATH + "/" + strTimeLog, localtime()), "a")
		while timeLog is TIME_LOG:
			newEditTxt = os.stat("temperature.txt").st_mtime
			if newEditTxt > lastEditTxt:
				oldLines = scriviFile(oldLines, fileBackup, virgola, campiJSON)
     
		fileBackup.close()
		timeLog = TIME_LOG
		virgola = False

	timeDir = TIME_DIR
	os.mkdir(os.mkdir(strftime(PATH, localtime())))

