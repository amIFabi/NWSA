import rrdtool, time
from SNMPAdmin import *

def slaGraph(agente):
	bd = rrdName + ".rrd"
	xml = rrdName + ".xml"

	# calculos de tiempo basado en la ultima entrada de la bd
	ultima_lectura = int(rrdtool.last(bd))
	tiempo_final = ultima_lectura
	tiempo_inicial = tiempo_final - 3600

	rrdtool.graph(rrdName + ".png",
								"--start", str(tiempo_inicial),
								"--end", str(tiempo_final),
								"--vertical-label=CPU Load",
								"--title=CPU usage",
								"--color", "ARROW#009900",
								'--vertical-label', "CPU usage (%)",
								'--lower-limit', '0',
								'--upper-limit', '100',
								"DEF:carga=" + bd + ":CPUload:AVERAGE",
								"AREA:carga#00FF00:CPU Load",
								"LINE1:30",
								"AREA:5#ff000022:stack",
								"VDEF:CPUlast=carga,LAST",
								"VDEF:CPUmin=carga,MINIMUM",
								"VDEF:CPUavg=carga,AVERAGE",
								"VDEF:CPUmax=carga,MAXIMUM",

								"COMMENT:Now          Min             Avg             Max",
								"GPRINT:CPUlast:%12.0lf%s",
								"GPRINT:CPUmin:%10.0lf%s",
								"GPRINT:CPUavg:%13.0lf%s",
								"GPRINT:CPUmax:%13.0lf%s",
								"VDEF:m=carga,LSLSLOPE",
								"VDEF:b=carga,LSLINT",
								'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
								"LINE2:tendencia#FFBB00")
	# grafica RAM
	rrdtool.graph(rrdName + ".png",
								"--start", str(tiempo_inicial),
								"--end", str(tiempo_final),
								"--vertical-label=RAM Load",
								"--title=RAM usage",
								"--color", "ARROW#009900",
								'--vertical-label', "RAM usage (%)",
								'--lower-limit', '0',
								'--upper-limit', '100',
								"DEF:carga=" + bd + ":RAMload:AVERAGE",
								"AREA:carga#00FF00:RAM Load",
								"LINE1:30",
								"AREA:5#ff000022:stack",
								"VDEF:RAMlast=carga,LAST",
								"VDEF:RAMmin=carga,MINIMUM",
								"VDEF:RAMavg=carga,AVERAGE",
								"VDEF:RAMmax=carga,MAXIMUM",

								"COMMENT:Now          Min             Avg             Max",
								"GPRINT:RAMlast:%12.0lf%s",
								"GPRINT:RAMmin:%10.0lf%s",
								"GPRINT:RAMavg:%13.0lf%s",
								"GPRINT:RAMmax:%13.0lf%s",
								"VDEF:m=carga,LSLSLOPE",
								"VDEF:b=carga,LSLINT",
								'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
								"LINE2:tendencia#FFBB00")
	# grafica HDD
	rrdtool.graph(rrdName + ".png",
								"--start", str(tiempo_inicial),
								"--end", str(tiempo_final),
								"--vertical-label=HDD Load",
								"--title=HDD usage",
								"--color", "ARROW#009900",
								'--vertical-label', "HDD usage (%)",
								'--lower-limit', '0',
								'--upper-limit', '100',
								"DEF:carga=" + bd + ":HDDload:AVERAGE",
								"AREA:carga#00FF00:HDD Load",
								"LINE1:30",
								"AREA:5#ff000022:stack",
								"VDEF:HDDlast=carga,LAST",
								"VDEF:HDDmin=carga,MINIMUM",
								"VDEF:HDDavg=carga,AVERAGE",
								"VDEF:HDDmax=carga,MAXIMUM",

								"COMMENT:Now          Min             Avg             Max",
								"GPRINT:HDDlast:%12.0lf%s",
								"GPRINT:HDDmin:%10.0lf%s",
								"GPRINT:HDDavg:%13.0lf%s",
								"GPRINT:HDDmax:%13.0lf%s",
								"VDEF:m=carga,LSLSLOPE",
								"VDEF:b=carga,LSLINT",
								'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
								"LINE2:tendencia#FFBB00")

	rrdtool.graph(rrdName + ".png",
								"--start", str(tiempo_inicial),
								"--end", str(tiempo_final),
								"--vertical-label=Processes",
								"--title=Active processes",
								"--color", "ARROW#009900",
								'--vertical-label', "Number of processes",
								'--lower-limit', '0',
								'--upper-limit', '100',
								"DEF:carga=" + bd + ":Processes:AVERAGE",
								"AREA:carga#00FF00:Processes",
								"LINE1:30",
								"AREA:5#ff000022:stack",
								"VDEF:HDDlast=carga,LAST",
								"VDEF:HDDmin=carga,MINIMUM",
								"VDEF:HDDavg=carga,AVERAGE",
								"VDEF:HDDmax=carga,MAXIMUM",

								"COMMENT:Now          Min             Avg             Max",
								"GPRINT:HDDlast:%12.0lf%s",
								"GPRINT:HDDmin:%10.0lf%s",
								"GPRINT:HDDavg:%13.0lf%s",
								"GPRINT:HDDmax:%13.0lf%s",
								"VDEF:m=carga,LSLSLOPE",
								"VDEF:b=carga,LSLINT",
								'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
								"LINE2:tendencia#FFBB00")

	rrdtool.graph(rrdName + ".png",
								"--start", str(tiempo_inicial),
								"--end", str(tiempo_final),
								"--vertical-label=HDD Load",
								"--title=HDD usage",
								"--color", "ARROW#009900",
								'--vertical-label', "HDD usage (%)",
								'--lower-limit', '0',
								'--upper-limit', '100',
								"DEF:carga=" + bd + ":HDDload:AVERAGE",
								"AREA:carga#00FF00:HDD Load",
								"LINE1:30",
								"AREA:5#ff000022:stack",
								"VDEF:HDDlast=carga,LAST",
								"VDEF:HDDmin=carga,MINIMUM",
								"VDEF:HDDavg=carga,AVERAGE",
								"VDEF:HDDmax=carga,MAXIMUM",

								"COMMENT:Now          Min             Avg             Max",
								"GPRINT:HDDlast:%12.0lf%s",
								"GPRINT:HDDmin:%10.0lf%s",
								"GPRINT:HDDavg:%13.0lf%s",
								"GPRINT:HDDmax:%13.0lf%s",
								"VDEF:m=carga,LSLSLOPE",
								"VDEF:b=carga,LSLINT",
								'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
								"LINE2:tendencia#FFBB00")

hostaddr = str(input("Introduce IP: "))
community = str(input("Introduce community: "))
interface = str(input("Introduce interface: "))
des = snmpGet(community, hostaddr, ("1.3.6.1.2.1.2.2.1.2." + interface))
aux = des.split(" ")
des = aux[0]
rrdName = hostaddr + des
agent = {"community": community, "hostaddr": hostaddr, "if": interface, "desc": des, "rrdName": rrdName}