import sys, rrdtool, time, os, MongoAdmin
from pysnmp.hlapi import *
from reportlab.pdfgen import canvas

class OID:

	oid = ""
	name = ""
	interface = False
	desc = ""

	def __init__(self, oid, name, interface, desc):
		self.oid = oid
		self.name = name
		self.interface = interface
		self.desc = desc

def createRRD(rrdName, step="60", ds=["DS:ifOutUcastPkts:COUNTER:600:U:U"], rra="RRA:AVERAGE:0.5:1:600"):
	rrdFile = rrdName + ".rrd"
	xmlFile = rrdName + ".xml"
	ret = rrdtool.create(rrdFile, "--start", "N", "--step", step, ds[0], rra)
	if(len(ds) > 1):
		for i in range(1, len(ds)):
			print(ds[i])
			addDataSource(rrdFile, ds[i])
	
	#"DS:ipInReceives:COUNTER:600:U:U",
	#"DS:icmpInEchoes:COUNTER:600:U:U",
	#"DS:tcpInSegs:COUNTER:600:U:U",
	#"DS:udpInDatagrams:COUNTER:600:U:U",

	dumpRRD(rrdFile, xmlFile)
	if ret:
		print(rrdtool.error())
	else:
		print("--------------------------------------------------")
		print("RRD created")
		print("--------------------------------------------------")

def addDataSource(rrdFile, dsSpec):
	rrdtool.tune(rrdFile, dsSpec)

def addRRA(rrdFile, rraSpec):
	rrdtool.tune(rrdFile, rraSpec)

def dumpRRD(rrdFile, xmlFile):
	rrdtool.dump(rrdFile, xmlFile)
	print("--------------------------------------------------")
	print("RRD dumped")
	print("--------------------------------------------------")

def snmpGet(community, host, oid):
	varBinds = getCmd(SnmpEngine(), 
						CommunityData(community), 
						UdpTransportTarget((host, 161)), 
						ContextData(), 
						ObjectType(ObjectIdentity(oid)))

	mib = str(next(varBinds)[3][0])
	
	return mib.split(sep=' = ')[1]

def updateRRD(agent, oids):
	while 1:
		x = MongoAdmin.getHost(agent)
		if(x == None):
			break
		value = []
		row = "N:"
		for mib in oids:
			if(mib.interface):
				resp = snmpGet(x["community"], x["hostaddr"], (mib.oid + "." + x["if"]))
			else:
				resp = snmpGet(x["community"], x["hostaddr"], mib.oid)
			
			if(resp == "No Such Object currently exists at this OID"):
				resp = "0"

			value.append(resp)

		row = row + ":".join(value)
		#print(row)
		
		rrdtool.update("rrd/" + x["rrdName"] + ".rrd", row)
		rrdtool.dump("rrd/" + x["rrdName"] + ".rrd", "xml/" + x["rrdName"] + ".xml")
		time.sleep(1)

def graphRRD(minutes, rrdName):
	aux = int(minutes)
	tiempoA = int(time.time())
	tiempoInicio = tiempoA - (60 * aux)  # 5 min = 600 s

	oids = MongoAdmin.getOIDS()
	for x in oids:
		rrdtool.graph("graphs/" + rrdName + x["name"] + ".png", "--start", str(tiempoInicio),
									"--vertical-label=Bytes/s",
									"--width", "500",
									"--height", "250",
									"--zoom", "10",
									"--full-size-mode",
									"--title=" + x["desc"],
									"DEF:input=rrd/" + rrdName + ".rrd:" + x["name"] + ":AVERAGE",
									"AREA:input#00FF00:" + x["name"] + " \r")

	"""
	ret1 = rrdtool.graph(rrdName+"_1.png", "--start", str(tiempoInicio),
											"--vertical-label=Bytes/s",
											"--width", "500",
											"--height", "250",
											"--zoom", "10",
											"--full-size-mode",
											"--title=Paquetes Unicast que ha recibido la interfaz",
											"DEF:entrada="+rrdName+".rrd:inUnicastInterfaz:AVERAGE",
											"AREA:entrada#00FF00:Paquetes Unicast \r")

	ret2 = rrdtool.graph(rrdName + "_2.png", "--start", str(tiempoInicio),
												"--vertical-label=Bytes/s",
												"--width", "500",
												"--height", "250",
												"--zoom", "10",
												"--full-size-mode",
												"--title=Paquetes recibidos a protocolos PIv4",
												"DEF:entrada=" + rrdName + ".rrd:inIpv4:AVERAGE",
												"AREA:entrada#00FF00:Paquetes IPv4 \r")

	ret3 = rrdtool.graph(rrdName + "_3.png", "--start", str(tiempoInicio),
												"--vertical-label=Bytes/s",
												"--width", "500",
												"--height", "250",
												"--zoom", "10",
												"--full-size-mode",
												"--title=Mensajes ICMP echo que ha enviado el agente",                      
												"DEF:entrada=" + rrdName + ".rrd:inEchoSsnmp:AVERAGE",
												"AREA:entrada#00FF00:Mensajes ICMP \r")

	ret4 = rrdtool.graph(rrdName + "_4.png", "--start", str(tiempoInicio),
											"--vertical-label=Bytes/s",
											"--width", "500",
											"--height", "250",
											"--zoom", "10",
											"--full-size-mode",
											"--title=Segmentos TCP recibidos",
											"DEF:entrada=" + rrdName + ".rrd:inTcp:AVERAGE",
											"AREA:entrada#00FF00:Segmentos TCP \r")

	ret5 = rrdtool.graph(rrdName + "_5.png", "--start", str(tiempoInicio),
											"--vertical-label=Bytes/s",
											"--width", "500",
											"--height", "250",
											"--zoom", "10",
											"--full-size-mode",
											"--title=Datagramas entragados a usuarios UDP",
											"DEF:entrada=" + rrdName + ".rrd:datagramUDP:AVERAGE",
											"AREA:entrada#00FF00:Datagramas UDP \r")
	"""

def createPDF(agent):
	oids = MongoAdmin.getOIDS()

	ops = snmpGet(agent["community"], agent["hostaddr"], "1.3.6.1.2.1.1.1.0")
	loc = snmpGet(agent["community"], agent["hostaddr"], "1.3.6.1.2.1.1.6.0")
	time = int(snmpGet(agent["community"], agent["hostaddr"], "1.3.6.1.2.1.1.3.0"))
	numports = snmpGet(agent["community"], agent["hostaddr"], "1.3.6.1.2.1.2.1.0")

	time = int(time // 60)

	pdf = canvas.Canvas(agent["rrdName"] + ".pdf")
	pdf.setLineWidth(.3)
	pdf.setFont('Helvetica', 12)

	pdf.drawString(30, 750, "OS: " + ops)
	pdf.drawString(30, 735, "Location: " + loc)
	pdf.drawString(30, 720, "Interfaces: " + numports)
	pdf.drawString(30, 705, "Up time: " + str(time) + " min." )
	pdf.drawString(30, 690, "Community: " + agent["community"])
	pdf.drawString(30, 675, "IP: " + agent["hostaddr"])

	for i in oids:
		pdf.drawImage("graphs/" + agent["rrdName"] + agent["name"] + ".png", 30, 555, 250, 100)

	pdf.save()

	#agentstatus = str(snmpGet("fabo", "127.0.0.1", '1.3.6.1.2.1.2.2.1.8.1'))
	#print("Agent Status: " + str(agentstatus))