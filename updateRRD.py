import time
import rrdtool
from getSNMP import consultaSNMP

totalInTraf = 0
totalOutTraf = 0

while 1:
  totalInTraf = int(consultaSNMP("fabo", "localhost", "1.3.6.1.2.1.2.2.1.10.8"))
  totalOutTraf = int(consultaSNMP("fabo", "localhost", "1.3.6.1.2.1.2.2.1.16.8"))

  valor = "N:" + str(totalInTraf) + ":" + str(totalOutTraf)
  print (valor)
  rrdtool.update("trafico.rrd", valor)
  rrdtool.dump("trafico.rrd", "trafico.xml")
  time.sleep(1)

if ret:
    print (rrdtool.error())
    time.sleep(300)