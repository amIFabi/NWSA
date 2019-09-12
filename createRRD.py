import rrdtool

ret = rrdtool.create("trafico.rrd", 
										"--start", "N", 
										"--step", "300", 
										"DS:inoctets:COUNTER:600:U:U", "DS:outoctets:COUNTER:600:U:U",
										"RRA:AVERAGE:0.5:6:700", "RRA:AVERAGE:0.5:1:600")

rrdtool.dump("trafico.rrd", "trafico.xml")

if ret:
	print (rrdtool.error())
