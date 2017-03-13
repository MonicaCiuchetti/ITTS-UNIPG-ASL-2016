###############################
### Librerie                ###
###############################
import os
import io
from time import localtime, strftime
from datetime import datetime
import json

import avro.schema
from avro.io import DatumWriter

from kafka import KafkaProducer

###############################
### Funzioni                ###
###############################

#restituisce minuto attuale
def pickMinute():
	return datetime.now().minute

#restituisce ora attuale
def pickHour():
	return datetime.now().hour

#restituisce giorno attuale
def pickDay():
	return datetime.now().day

#scrive file backup, formatta in avro e spedisce su kafka
def scriviFile(oldLines, newFile):
	mini = open(MINICOM_FILE, "r")
	data = mini.readlines()
	mini.close()
	newLines = len(data)
	
	while oldLines < newLines - 1:
		riga = data[oldLines].replace("\n", "")
		stringaJSON = getJSON(riga)

		backup = open(strftime(PATH + "/" + strTimeLog, localtime()), "a")
		if newFile:
			newFile = False
		else:
			backup.write(',')
		backup.write(stringaJSON)
		backup.close()
		sendToKafka(stringaJSON)
		oldLines += 1

	return oldLines

def getJSON(line):
	lista = line.split("   ")

	if len(lista) != len(campiJSON):
		raise ValueError("Schema diverso da campi del minicom!")

	stringaJSON = '{'
	for i in range(len(campiJSON)):
		stringaJSON += '"' + campiJSON[i]['name'] + '": '
		if campiJSON[i]['type'] != "string":
			stringaJSON += lista[i]
		else:
			stringaJSON += '"' + lista[i] + '"'
		stringaJSON += ','
	stringaJSON = stringaJSON[:-1] + '}'

	return stringaJSON

def sendToKafka(stringaJSON):
	oggettoJSON = json.loads(stringaJSON, encoding="utf-8")

	schema = avro.schema.parse(open("schema-prova.avsc", "rb").read())
	writer = avro.io.DatumWriter(schema)
	bytes_writer = io.BytesIO()
	encoder = avro.io.BinaryEncoder(bytes_writer)

	writer.write(oggettoJSON, encoder)

	producer = KafkaProducer(bootstrap_servers=KAFKA_SOCK)
	producer.send(KAFKA_TOPIC_NAME, bytes_writer.getvalue())
	producer.flush()

###############################
### Parametri               ###
###############################
TIME_LOG = "minuto"
TIME_DIR = "ora"
AVRO_SCHEMA = "schema-prova.avsc"
LOG_PATH = "/home/asl-2016"
MINICOM_FILE = "temperature.txt"
KAFKA_SOCK = "localhost:9092"
KAFKA_TOPIC_NAME = "nometopic"

if TIME_LOG == "minuto":
	TIME_LOG = pickMinute
	strTimeLog = "%Y-%m-%d-%H:%M.json"
elif TIME_LOG == "ora":
	TIME_LOG = pickHour
	strTimeLog = "%Y-%m-%d-%H:00.json"
else:
	raise ValueError("formato orario errato")

if TIME_DIR == "ora":
	TIME_DIR = pickHour
	strTimeDir = "%Y-%m-%d-%H:00"
elif TIME_DIR == "giorno":
	TIME_DIR = pickDay
	strTimeDir = "%Y-%m-%d"
else:
	raise ValueError("formato orario errato")

PATH = LOG_PATH + "/" + strTimeDir
campiJSON = json.loads(open(AVRO_SCHEMA, "r").read())['fields']

###############################
### MAIN                    ###
###############################
def main():
	oldLines = 0
	lastEditTxt = os.stat(MINICOM_FILE).st_mtime

	timeLog = TIME_LOG()
	timeDir = TIME_DIR()

	temp = strftime(PATH, localtime())
	if not os.path.isdir(temp):
		os.mkdir(temp)

	while True:
		while timeDir == TIME_DIR():
			newFile = True
			timeLog = TIME_LOG()
			while timeLog == TIME_LOG():
				newEditTxt = os.stat(MINICOM_FILE).st_mtime
				if newEditTxt > lastEditTxt:
					oldLines = scriviFile(oldLines, newFile)
					lastEditTxt = newEditTxt
					newFile = False
		
		timeDir = TIME_DIR()

		temp = strftime(PATH, localtime())
		if not os.path.isdir(temp):
			os.mkdir(temp)

if __name__ == "__main__":
	main()