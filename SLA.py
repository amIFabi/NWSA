import sys, threading, os.path, MongoAdmin
from reportlab.pdfgen import canvas
from os import remove
from SNMPAdmin import *

def updateCPUValues(agent, oids):
	while 1:
		value = []
		row = "N:"
		for mib in oids:
			#print(mib.oid)
			resp = snmpGet(agent["community"], agent["hostaddr"], mib.oid)
			
			if(resp == "No Such Object currently exists at this OID"):
				resp = "0"

			value.append(resp)

		row = row + ":".join(value)
		#print(row)
		
		rrdtool.update(agent["rrdName"] + "CPULoad" + ".rrd", row)
		rrdtool.dump(agent["rrdName"] + "CPULoad" + ".rrd", agent["rrdName"] + "CPULoad" + ".xml")
		time.sleep(1)

def updateRAMValues(agent):
	while 1:
		usedRAM = float(snmpGet(agent["community"], agent["hostaddr"], "1.3.6.1.4.1.2021.4.11.0"))
		totalRAM = float(snmpGet(agent["community"], agent["hostaddr"], "1.3.6.1.4.1.2021.4.5.0"))
		# print(str(totalRAM) + ":" + str(usedRAM))
		loadRAM = ((totalRAM - usedRAM) * 100) / totalRAM
		row = "N:" + str(loadRAM)

		rrdtool.update(agent["rrdName"] + "RAMLoad" + ".rrd", row)
		rrdtool.dump(agent["rrdName"] + "RAMLoad" + ".rrd", agent["rrdName"] + "RAMLoad" + ".xml")
		time.sleep(1)

def updateHDDValues(agent):
	while 1:
		loadHDD = float(snmpGet(agent["community"], agent["hostaddr"], "1.3.6.1.2.1.25.2.3.1.6.1"))
		loadHDD = loadHDD / (1024 * 1024)
		row = "N:" + str(loadHDD)

		rrdtool.update(agent["rrdName"] + "HDDLoad" + ".rrd", row)
		rrdtool.dump(agent["rrdName"] + "HDDLoad" + ".rrd", agent["rrdName"] + "HDDLoad" + ".xml")
		time.sleep(1)

def updateProcValues(agent):
	while 1:
		#hrSystemProcess 1.3.6.1.2.1.25.1.6.0
		#hrSytemMaxProcesses 1.3.6.1.2.1.25.7.0
		process = float(snmpGet(agent["community"], agent["hostaddr"], "1.3.6.1.2.1.25.1.6.0"))
		maxprocess = float(snmpGet(agent["community"], agent["hostaddr"], "1.3.6.1.2.1.25.1.7.0"))
		processPer = (process * 100) / maxprocess
		row = "N:" + str(processPer)

		rrdtool.update(agent["rrdName"] + "Process" + ".rrd", row)
		rrdtool.dump(agent["rrdName"] + "Process" + ".rrd", agent["rrdName"] + "RAMLoad" + ".xml")
		time.sleep(1)

def updateTCPValues(agent):
	while 1:
		# 1.3.6.1.2.1.6.9.0
		tcpConn = int(snmpGet(agent["community"], agent["hostaddr"], "1.3.6.1.2.1.6.9.0"))
		row = "N:" + str(tcpConn)

		rrdtool.update(agent["rrdName"] + "TCPConn" + ".rrd", row)
		rrdtool.dump(agent["rrdName"] + "TCPConn" + ".rrd", agent["rrdName"] + "TCPConn" + ".xml")
		time.sleep(1)

def updateLocationValue(agent):
	location = snmpGet(agent["community"], agent["hostaddr"], "1.3.6.1.2.1.1.6.0")
	if(location == "Unknown"):
		print("The location is Unknown please configure a valid location")

def getCores(agent):
	coreOids = []
	coreLoad = OID("1.3.6.1.2.1.25.3.3.1.2.196608", "CPULoad196608", False, "Percentage in use of the core 196608")
	coreOids.append(coreLoad)
	core = 196608
	while(True):
		core += 1
		resp = snmpGet(agent["community"], agent["hostaddr"], ("1.3.6.1.2.1.25.3.3.1.2." + str(core)))
		if(resp != "No Such Instance currently exists at this OID"):
			coreLoad = OID("1.3.6.1.2.1.25.3.3.1.2." + str(core), "CPULoad" + str(core), False, "Percentage in use of the core" + str(core))
			coreOids.append(coreLoad)
		else:
			break

	# for i in coreOids:
	# 	print(i.oid)

	return coreOids

def setupAgent():
	hostaddr = str(input("Introduce IP: "))
	community = str(input("Introduce community: "))
	interface = str(input("Introduce interface: "))
	des = snmpGet(community, hostaddr, ("1.3.6.1.2.1.2.2.1.2." + interface))
	aux = des.split(" ")
	des = aux[0]
	rrdName = hostaddr + des
	agent = {"community": community, "hostaddr": hostaddr, "if": interface, "desc": des, "rrdName": rrdName}
	threads = []
	#MongoAdmin.addHost(agent)

	agentThread = threading.Thread(target=updateLocationValue, args=(agent, ))
	agentThread.start()

	coresOIDs = getCores(agent)
	print(str(len(coresOIDs)) + " cores")
	ds = []
	for i in coresOIDs:
		s = "DS:" + i.name + ":GAUGE:600:U:U"
		ds.append(s)

	createRRD(rrdName + "CPULoad", ds=ds, rra="RRA:AVERAGE:0.5:1:24")
	cputhread = threading.Thread(target=updateCPUValues, args=(agent, coresOIDs))
	cputhread.start()
	threads.append(cputhread)

	ds = ["DS:RAMLoad:GAUGE:600:U:U"]
	createRRD(rrdName + "RAMLoad", ds=ds, rra="RRA:AVERAGE:0.5:1:24")
	ramthread = threading.Thread(target=updateRAMValues, args=(agent, ))
	ramthread.start()
	threads.append(ramthread)

	ds = ["DS:HDDLoad:GAUGE:600:U:U"]
	createRRD(rrdName + "HDDLoad", ds=ds, rra="RRA:AVERAGE:0.5:1:24")
	hddthread = threading.Thread(target=updateHDDValues, args=(agent, ))
	hddthread.start()
	threads.append(hddthread)

	ds = ["DS:Process:GAUGE:600:U:U"]
	createRRD(rrdName + "Process", ds=ds, rra="RRA:AVERAGE:0.5:1:24")
	processthread = threading.Thread(target=updateProcValues, args=(agent, ))
	processthread.start()
	threads.append(processthread)

	ds = ["DS:TCPConn:GAUGE:600:U:U"]
	createRRD(rrdName + "TCPConn", ds=ds, rra="RRA:AVERAGE:0.5:1:24")
	tcpthread = threading.Thread(target=updateTCPValues, args=(agent, ))
	tcpthread.start()
	threads.append(tcpthread)


setupAgent()
# hostaddr = str(input("Introduce IP: "))
# community = str(input("Introduce community: "))
# interface = str(input("Introduce interface: "))
# des = snmpGet(community, hostaddr, ("1.3.6.1.2.1.2.2.1.2." + interface))
# aux = des.split(" ")
# des = aux[0]
# rrdName = hostaddr + des
# agent = {"community": community, "hostaddr": hostaddr, "if": interface, "desc": des, "rrdName": rrdName}
# getCores(agent)