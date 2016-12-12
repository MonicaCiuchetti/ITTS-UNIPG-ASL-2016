import time
x = 0
riga = ""
while True:
	temperature_txt = open("temperature.txt","a")
	riga = str(x) + "   " + str(x) + "\n"
	time.sleep(1)
	temperature_txt.write(riga)
	print riga
	x = x + 1
	temperature_txt.close()
	

