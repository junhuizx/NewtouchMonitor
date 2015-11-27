#-*-coding: utf-8-*-
import netsnmp
import logging


# host = "localhost"
# precision
PRECISION = 2

class snmpOprt(object):

	def __init__(self, HostId):
		
		self.session = netsnmp.Session(Version=2,DestHost=HostId,
							   Community='public')
		
		SysDesc = '.1.3.6.1.2.1.1.1.0'
		oid1 = netsnmp.Varbind(SysDesc,'',5,'INTEGER')
		getOidList = netsnmp.VarList(oid1)
		try:
			result = self.session.get(getOidList)
			print result
		except Exception, error:
			logging.warning('Fial to connect host: ' + HostId)
			raise error

	def __walk(self, oidNumb):
		# print oidNumb
		# oid = netsnmp.Varbind(oidNumb,'',10,'INTEGER')
		oidVar = netsnmp.VarList(netsnmp.Varbind(oidNumb,'',10,'INTEGER'))
		return self.session.walk(oidVar)

	def getCpuData(self):
		# Get Access
		ssCpuIdle = '.1.3.6.1.4.1.2021.11.11.0'
		Load5 = '.1.3.6.1.4.1.2021.10.1.3.1'

		oid1 = netsnmp.Varbind(ssCpuIdle,'',10,'INTEGER')
		oid2 = netsnmp.Varbind(Load5,'',10,'INTEGER')
		getOidList = netsnmp.VarList(oid1, oid2)

		# oid2 = netsnmp.Varbind(hrProcessorLoad,'',10,'INTEGER')
		# walkOidList = netsnmp.VarList(oid2)

		result = self.session.get(getOidList)
		cpuUsage = str(100 - int(result[0]))
		return {'cpuUsage':cpuUsage+'%', 'load':str(result[1])}


	def getMemoryData(self):
		# Get Access
		memTotalReal = '.1.3.6.1.4.1.2021.4.5.0'
		memAvailReal = '.1.3.6.1.4.1.2021.4.6.0'
		
		oid1 = netsnmp.Varbind(memTotalReal,'',10,'INTEGER')
		oid2 = netsnmp.Varbind(memAvailReal,'',10,'INTEGER')
		getOidList = netsnmp.VarList(oid1, oid2)
		result = self.session.get(getOidList)
		
		total = round(float(result[0])/1024**2, PRECISION)
		used = round(float(int(result[0])-int(result[1]))/1024**2, PRECISION)
		usage = round(used*100/total, PRECISION)

		return {'memTotal':str(total)+'G', 'memUsed':str(used)+'G',
				'memUsage' : str(usage)+'%'}


	def getDiskData(self):
		# Walk Access
		dskDevice = '.1.3.6.1.4.1.2021.9.1.3'
		dskTotal = '.1.3.6.1.4.1.2021.9.1.6'
		dskUsed = '.1.3.6.1.4.1.2021.9.1.8'

		total = round(float(self.__walk(dskTotal)[0])/(1024**2), PRECISION)
		used = round(float(self.__walk(dskUsed)[0])/(1024**2), PRECISION)
		usage = round(used/total * 100, PRECISION)

		return {'diskDevice' : str(self.__walk(dskDevice)[0]),
				'diskTotal':str(total)+'G',
				'diskUsed' :str(used)+'G',
				'diskUsage':str(usage)+'%' }



	def getIFData(self):
		# Walk Access
		IfDescr = '.1.3.6.1.2.1.2.2.1.2'
		IfOperStatus = '.1.3.6.1.2.1.2.2.1.8'
		IfInOctet = '.1.3.6.1.2.1.2.2.1.10'
		IfOutOctet = '.1.3.6.1.2.1.2.2.1.16'

		ifName = self.__walk(IfDescr)
		ifStatus = self.__walk(IfOperStatus)
		ifIn = self.__walk(IfInOctet)
		ifOut = self.__walk(IfOutOctet)

		result = {}
		for pos, value in enumerate(ifStatus):
			if value == '2':
				break
			result[ifName[pos]] = {'ifIn' : str(ifIn[pos]), 
								   'ifOut': str(ifOut[pos])} 
		return result


	def getLoadData(self):
# 		Get Access
		Load5 = '.1.3.6.1.4.1.2021.10.1.3.1'
		Load10 = '.1.3.6.1.4.1.2021.10.1.3.2'
		Load15 = '.1.3.6.1.4.1.2021.10.1.3.3'
		
		oid1 = netsnmp.Varbind(Load5,'',10,'INTEGER')
		oid2 = netsnmp.Varbind(Load10,'',10,'INTEGER')
		oid3 = netsnmp.Varbind(Load15,'',10,'INTEGER')
		
		getOidList = netsnmp.VarList(oid1, oid2, oid3)
		result = self.session.get(getOidList)
		
		return {'load5':str(result[0]), 
				'load10':str(result[1]), 
				'load15':str(result[2])}
		
		
	def getProcNumb(self):
# 		Work Access
# 		process list
# 		hrSWRunName = '.1.3.6.1.2.1.25.4.2.1.2'
		procNumb = '.1.3.6.1.2.1.25.1.6' 
		
		return {'procNumb' : self.__walk(procNumb)[0]}
		
if __name__ == '__main__':
	host = '192.168.205.112'
	obj = snmpOprt(host)
# 	print obj.getDiskData()
# 	print obj
	# obj = snmpOprt('1.1.1.1')
# 	print obj.getCpuData()
# 	print obj.getMemoryData()
# 	print obj.getLoadData()
	print obj.getIFData()
# 	print obj.getProcNumb()