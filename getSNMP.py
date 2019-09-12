from pysnmp.hlapi import *
import time

def consultaSNMP(community, host, oid):
	errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),
	CommunityData(community),
	UdpTransportTarget((host, 161)),
	ContextData(),
	ObjectType(ObjectIdentity(oid))))

	if errorIndication:
		print(errorIndication)
	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
	else:
		for varBind in varBinds:
			varB = (' = '.join([x.prettyPrint() for x in varBind]))
			resultado = varB.split()[2]
	
	return resultado

"""
while True:
    print(consultaSNMP("fabo", "localhost", "1.3.6.1.2.1.2.2.1.16.1"))
    print(consultaSNMP("fabo", "localhost", "1.3.6.1.2.1.2.2.1.10.1"))
    time.sleep(2)
"""