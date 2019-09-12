import sys
import rrdtool
import time

tiempo_actual = int(time.time())
tiempo_final = tiempo_actual - 86400
tiempo_inicial = tiempo_final -25920000

while 1:
	ret = rrdtool.graph( "trafico.png",
											"--start",'1567002480',
 #                    "--end","N",
											"--vertical-label=Bytes/s",
											"--width", "250",
											"--height", "125",
											"--zoom", "10",
											"--full-size-mode",
											"DEF:inoctets=trafico.rrd:inoctets:AVERAGE",
											"DEF:outoctets=trafico.rrd:outoctets:AVERAGE",
											"AREA:inoctets#00FF00:In traffic",
											"LINE1:outoctets#0000FF:Out traffic\r")

		time.sleep(30)