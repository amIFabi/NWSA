import sys, threading, os.path, SNMPAdmin, MongoAdmin
from os import remove
from reportlab.pdfgen import canvas
#cpuload 1.3.6.1.2.1.25.3.3.1.2.196608
#ramload 1.3.6.1.2.1.
#hrSystemProcess 1.3.6.1.2.1.25.1.6 
#hrSytemMaxProcesses 1.3.6.1.2.1.25.6
#active-fan: .1.3.6.1.4.1.14988.1.1.3.9.0
#voltage: .1.3.6.1.4.1.14988.1.1.3.8.0
#temperature: .1.3.6.1.4.1.14988.1.1.3.10.0
#processor-temperature: .1.3.6.1.4.1.14988.1.1.3.11.0


def startMonitor():
	hosts = MongoAdmin.getHosts()
	if(hosts != None):
		for x in hosts:
			agentThread = threading.Thread(target=SNMPAdmin.updateRRD, args=(x["rrdName"], ))
			agentThread.start()

def addAgent():
	hostaddr = str(input("Introduce IP: "))
	community = str(input("Introduce community: "))
	interface = str(input("Introduce interface: "))
	des = SNMPAdmin.snmpGet(community, hostaddr, ("1.3.6.1.2.1.2.2.1.2." + interface))
	rrdName = hostaddr + des
	agent = {"community": community, "hostaddr": hostaddr, "if": interface, "desc": des, "rrdName": rrdName}

	MongoAdmin.addHost(agent)
	SNMPAdmin.createRRD(rrdName, ds=["DS:CPULoad1:GAUGE:600:0:100"], "RRA:AVERAGE:0.5:1:24")

	agentThread = threading.Thread(target=SNMPAdmin.updateRRD, args=(agent["rrdName"], ))
	agentThread.start()

	print("Agent added")

def deleteAgent():
	hostaddr = str(input("Introduce IP: "))
	community = str(input("Introduce community: "))
	interface = str(input("Introduce interface: "))
	des = SNMPAdmin.snmpGet(community, hostaddr, ("1.3.6.1.2.1.2.2.1.2." + interface))
	rrdName = hostaddr + des
	host = {"rrdName": rrdName}
	MongoAdmin.deleteHost(host)

def showAgents():
	hosts = MongoAdmin.getHosts()
	if(hosts != None):
		for h in hosts:
			print("--------------------------------------------------------------------------------------")
			print("System desc: " + SNMPAdmin.snmpGet(h["community"], h["hostaddr"], "1.3.6.1.2.1.1.1.0"))
			print("host address: " + h["hostaddr"] + " community: " + h["community"] + " interface: " + h["desc"])
			print("--------------------------------------------------------------------------------------")

def generateReport():
	hostaddr = str(input("Introduce IP: "))
	community = str(input("Introduce community: "))
	interface = str(input("Introduce interface: "))
	des = SNMPAdmin.snmpGet(community, hostaddr, ("1.3.6.1.2.1.2.2.1.2." + interface))
	rrdName = hostaddr + des
	host = {"rrdName": rrdName}
	agent = MongoAdmin.getHost(rrdName)
	print(agent)
	
	SNMPAdmin.graphRRD(10, rrdName)
	#SNMPAdmin.createPDF(agent)
	#print("Report created\n")

startMonitor()
while(True):
	print("1.- Add agent")
	print("2.- Delete agent")
	print("3.- Create report")
	print("4.- Show agents")
	option = int(input())

	if(option == 1):
		addAgent()
	elif(option == 2):
		deleteAgent()
	elif(option == 3):
		generateReport()
	elif(option == 4):
		showAgents()
	else:
		print("Choose valid option \n")