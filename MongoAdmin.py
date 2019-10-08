import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["nwadmin"]
hostCollection = db["host"]
oidCollection = db["oid"]

def addHost(host={"community": "fabo", "hostaddr": "localhost", "if": "8", "desc": "en1", "rrdName": "localhosten1"}):
	if(hostCollection.count_documents(host)):
		print("--------------------------------------------------")
		print("Host is already in the collection")
		print("--------------------------------------------------")
	else:
		x = hostCollection.insert_one(host)
		print("--------------------------------------------------")
		print("Host added: " + str(host["rrdName"]))
		print("--------------------------------------------------")

def deleteHost(host={"rrdName": "localhosten1"}):
	if(hostCollection.count_documents(host)):
		hosts = hostCollection.delete_one(host)
		print("--------------------------------------------------")
		print("Host deleted")
		print("--------------------------------------------------")
	else:
		print("--------------------------------------------------")
		print("Can't found host in the collection")
		print("--------------------------------------------------")

def deleteAllHost():
	hostCollection.delete_many({})

def getHosts():
	if(hostCollection.count_documents({})):
		return hostCollection.find()
	else:
		print("--------------------------------------------------")
		print("No Hosts in the collection")
		print("--------------------------------------------------")
		return None

def getHost(agent="localhosten1"):
	if(hostCollection.count_documents({"rrdName": agent})):
		return next(hostCollection.find_one(agent))
	else:
		print("--------------------------------------------------")
		print("Can't fond host")
		print("--------------------------------------------------")
		return None

def addOID(oid={"oid": "1.3.6.1.2.1.1.3.0", "name": "sysUpTime", "if": False, "desc": "Time since the last re-initialized"}):
	if(oidCollection.count_documents(oid)):
		print("--------------------------------------------------")
		print("OID is already in the collection")
		print("--------------------------------------------------")
	else:
		x = oidCollection.insert_one(oid)
		print("--------------------------------------------------")
		print("OID saved: " + str(oid["name"]))
		print("--------------------------------------------------")

def deleteOID(oid={"name": "sysUpTime"}):
	if(oidCollection.count_documents(oid)):
		oids = oidCollection.delete_one(oid)
		print("--------------------------------------------------")
		print("Host deleted")
		print("--------------------------------------------------")
	else:
		print("--------------------------------------------------")
		print("Can't found OID")
		print("--------------------------------------------------")

def getOIDS():
	if(oidCollection.count_documents({})):
		return oidCollection.find()
	else:
		print("--------------------------------------------------")
		print("No OIDs in the collection")
		print("--------------------------------------------------")
		return None

def getOID(oid="sysUpTime"):
	if(oidCollection.count_documents({"name": oid})):
		return next(oidCollection.find_one({"name": oid}))
	else:
		print("--------------------------------------------------")
		print("Can't found OID in the collection")
		print("--------------------------------------------------")
		return None


"""
addOID({"oid": "1.3.6.1.2.1.2.2.1.17", "name": "ifOutUcastPkts", "if": True, "desc": "Total number of unicast packets received"})
addOID({"oid": "1.3.6.1.2.1.4.3.0", "name": "ipInReceives", "if": False, "desc": "Total number of datagrams received"})
addOID({"oid": "1.3.6.1.2.1.5.8.0", "name": "icmpInEchoes", "if": False, "desc": "The number of ICMP Echo messages received"})
addOID({"oid": "1.3.6.1.2.1.6.10.0", "name": "tcpInSegs", "if": False, "desc": "The total number of TCP segments received"})
addOID({"oid": "1.3.6.1.2.1.7.1.0", "name": "udpInDatagrams", "if": False, "desc": "The total number of UDP datagrams delivered"})
"""
"""
addOID({"oid": "1.3.6.1.2.1.25.3.3.1.196608", "name": "hrProcessorLoad", "if": False, "desc": "Processor load"})
addOID({"oid": "1.3.6.1.2.1.25.3.3.1.196609", "name": "hrProcessorLoad", "if": False, "desc": "Processor load"})
addOID({"oid": "1.3.6.1.2.1.25.3.3.1.196610", "name": "hrProcessorLoad", "if": False, "desc": "Processor load"})
addOID({"oid": "1.3.6.1.2.1.25.3.3.1.196611", "name": "hrProcessorLoad", "if": False, "desc": "Processor load"})
addOID({"oid": "1.3.6.1.2.1.25.3.3.1.196612", "name": "hrProcessorLoad", "if": False, "desc": "Processor load"})
addOID({"oid": "1.3.6.1.2.1.25.3.3.1.196613", "name": "hrProcessorLoad", "if": False, "desc": "Processor load"})
addOID({"oid": "1.3.6.1.2.1.25.3.3.1.196614", "name": "hrProcessorLoad", "if": False, "desc": "Processor load"})
addOID({"oid": "1.3.6.1.2.1.25.3.3.1.196615", "name": "hrProcessorLoad", "if": False, "desc": "Processor load"})
"""

