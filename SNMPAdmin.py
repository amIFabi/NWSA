import sys, rrdtool, time
from pysnmp.hlapi import *
from reportlab.pdfgen import canvas

def createRRD(rrdName):
	rrdFile = rrdName + ".rrd"
	xmlFile = rrdName + ".xml"
	ret = rrdtool.create(rrdFile, "--start", "N", "--step", "60",
											"DS:inUnicastInterfaz:COUNTER:600:U:U",
											"DS:inIpv4:COUNTER:600:U:U",
											"DS:inEchoSsnmp:COUNTER:600:U:U",
											"DS:inTcp:COUNTER:600:U:U",
											"DS:datagramUDP:COUNTER:600:U:U",
											"RRA:AVERAGE:0.5:1:600")

	dumpRRD(rrdFile, xmlFile)
	if ret:
		print(rrdtool.error())
	else:
		print("RRD created")

def addDataSource(rrdFile, dsSpec):
	rrdtool.tune(rrdFile, dsSpec)

def addRRA(rrdFile, rraSpec):
	rrdtool.tune(rrdFile, rraSpec)

def dumpRRD(rrdFile, xmlFile):
	rrdtool.dump(rrdFile, xmlFile)
	print("RRD dumped")

def snmpGet(community, host, oid):
	errorIndication, errorStatus, errorIndex, varBinds = getCmd(SnmpEngine(), 
																															CommunityData(community), 
																															UdpTransportTarget((host, 161)), 
																															ContextData(), 
																															ObjectType(ObjectIdentity(oid)))

	if errorIndication:
		print(errorIndication)
	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
	else:
		for varBind in varBinds:
			varB = (' = '.join([x.prettyPrint() for x in varBind]))
			resultado = varB.split()[2]
	
	return resultado
	#return next(varBinds)

def updateRRD(host, version, community, port):
	while 1:
		# ifOutUcastPkts. Tabla. Revisar
		paquetes_unicast_interfaz = int(snmpGet(community, host, '1.3.6.1.2.1.2.2.1.17.'+port))

    # ipInReceives. Escalar
		paquetes_input_ipv4 = int(snmpGet(community, host, '1.3.6.1.2.1.4.3.0'))

		# icmpInEchoes. Escalar
		mensajes_icmmp_echo = int(snmpGet(community, host, '1.3.6.1.2.1.5.8.0'))

		# tcpInSegs. Escalar
		total_input_traffic = int(snmpGet(community, host, '1.3.6.1.2.1.6.10.0'))

		# udpInDatagrams. Escalar
		datagrama_udp = 0

		valor = "N:" + str(paquetes_unicast_interfaz) + ':' + str(paquetes_input_ipv4) + ':' + str(mensajes_icmmp_echo) + ':' + str(total_input_traffic) + ':' + str(datagrama_udp)
    #print(valor)
		rrdtool.update(host + ".rrd", valor)
		rrdtool.dump(host + ".rrd", host + ".xml")
		time.sleep(1)

def graphRRD(minutes, host):
	aux = int(minutes)
	tiempoA = int(time.time())
	tiempoInicio = tiempoA - (60 * aux)  # 5 min = 600 s

	ret1 = rrdtool.graph(host+"_1.png", "--start", str(tiempoInicio),
											"--vertical-label=Bytes/s",
											"--width", "500",
											"--height", "250",
											"--zoom", "10",
											"--full-size-mode",
											"--title=Paquetes Unicast que ha recibido la interfaz",
											"DEF:entrada="+host+".rrd:inUnicastInterfaz:AVERAGE",
											"AREA:entrada#00FF00:Paquetes Unicast \r")

	ret2 = rrdtool.graph(host + "_2.png", "--start", str(tiempoInicio),
												"--vertical-label=Bytes/s",
												"--width", "500",
												"--height", "250",
												"--zoom", "10",
												"--full-size-mode",
												"--title=Paquetes recibidos a protocolos PIv4",
												"DEF:entrada=" + host + ".rrd:inIpv4:AVERAGE",
												"AREA:entrada#00FF00:Paquetes IPv4 \r")

	ret3 = rrdtool.graph(host + "_3.png", "--start", str(tiempoInicio),
												"--vertical-label=Bytes/s",
												"--width", "500",
												"--height", "250",
												"--zoom", "10",
												"--full-size-mode",
												"--title=Mensajes ICMP echo que ha enviado el agente",                      
												"DEF:entrada=" + host + ".rrd:inEchoSsnmp:AVERAGE",
												"AREA:entrada#00FF00:Mensajes ICMP \r")

	ret4 = rrdtool.graph(host + "_4.png", "--start", str(tiempoInicio),
											"--vertical-label=Bytes/s",
											"--width", "500",
											"--height", "250",
											"--zoom", "10",
											"--full-size-mode",
											"--title=Segmentos TCP recibidos",
											"DEF:entrada=" + host + ".rrd:inTcp:AVERAGE",
											"AREA:entrada#00FF00:Segmentos TCP \r")

	ret5 = rrdtool.graph(host + "_5.png", "--start", str(tiempoInicio),
											"--vertical-label=Bytes/s",
											"--width", "500",
											"--height", "250",
											"--zoom", "10",
											"--full-size-mode",
											"--title=Datagramas entragados a usuarios UDP",
											"DEF:entrada=" + host + ".rrd:datagramUDP:AVERAGE",
											"AREA:entrada#00FF00:Datagramas UDP \r")

def createPDF(host):
	archivo = open("agentes.txt", "r")  # Archivo de texto - escritura al final
	texto = archivo.read()  # Tenemos el archivo completo
	lista = texto.split("\n")
	for aux in lista:
		agente = aux.split(" ")
		if agente[0] == host:
			break

    #agente[0] - host
    #agente[1] - version
    #agente[2] - comunidad
    #agente[3] - puerto

	# sysDescr
	sistema_operativo = str(snmpGet(agente[2].replace(" ", ""), host.replace(" ", ""), '1.3.6.1.2.1.1.1.0'))

	# sysLocation
	ubicacion = str(snmpGet(agente[2].replace(" ", ""), host.replace(" ", ""), '1.3.6.1.2.1.1.6.0'))

	tiempo_actividad = int(snmpGet(agente[2].replace(" ", ""), host.replace(" ", ""), '1.3.6.1.2.1.1.3.0'))

	num_puertos = str(snmpGet(agente[2].replace(" ", ""), host.replace(" ", ""), '1.3.6.1.2.1.2.1.0'))

	pdf = canvas.Canvas("reporte-"+host+".pdf")
	pdf.setLineWidth(.3)
	pdf.setFont('Helvetica', 12)

	pdf.drawString(30, 750, "OS: " + sistema_operativo)
	pdf.drawString(30, 735, "Location: " + ubicacion)
	pdf.drawString(30, 720, "Interfaces: " + num_puertos)
	pdf.drawString(30, 705, "Up time: " +str(tiempo_actividad)+ " segundos" )
	pdf.drawString(30, 690, "Community: " + agente[2])
	pdf.drawString(30, 675, "IP: " + agente[0])

	pdf.drawImage(agente[0] + "_1.png", 30, 555, 250, 100)
	pdf.drawImage(agente[0] + "_2.png", 290, 555, 250, 100)
	pdf.drawImage(agente[0] + "_3.png", 30, 450, 250, 100)
	pdf.drawImage(agente[0] + "_4.png", 290, 450, 250, 100)
	pdf.drawImage(agente[0] + "_5.png", 30, 345, 250, 100)

	pdf.save()

	estatus_agente = str(snmpGet("fabo", "127.0.0.1", '1.3.6.1.2.1.2.2.1.8.1'))
	print("Agent Status: " + str(estatus_agente))

"""
createRRD("192.168.1.79")
addDataSource("192.168.1.79.rrd", "DS:inIpv4:COUNTER:600:U:U")
addDataSource("192.168.1.79.rrd", "DS:inEchoSsnmp:COUNTER:600:U:U")
addDataSource("192.168.1.79.rrd", "DS:inTcp:COUNTER:600:U:U")
addDataSource("192.168.1.79.rrd", "DS:datagramUDP:COUNTER:600:U:U")
dumpRRD("192.168.1.79.rrd", "192.168.1.79.xml")
#print(snmpGet("EricFabianPeraltaRamirez", "10.31.87.154", "1.3.6.1.2.1.1.1.0")[3][0].)

g = getCmd(SnmpEngine(), CommunityData("fabo"), UdpTransportTarget(("127.0.0.1", 161)), ContextData(), ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0")))

print(next(g)[3][0])
"""


