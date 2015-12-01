
#-*-coding:utf-8-*-
import redis
import logging
import time
import json

# Target redis host ip and port
HostIP = 'localhost'
Port = 6379
TimeFormat = '%Y-%m-%d-%X'

class RedisHashOprt(object):

	def __init__(self, host_ip, port_numb, db_numb=0):
		try:
			self.residDB = redis.Redis(host = host_ip, port=port_numb, db=db_numb)
			# print 'dbsize:%s' %self.residDB.dbsize()
			print 'Connect Successfully!\nRedis--Version' +\
				  self.residDB.info()['redis_version']
		except Exception, error:
			logging.warning('Fail to connet ' + HostIP + ' redis!') 
			raise error


	def setHash(self, hash_name, value_dic):
		try:
			self.residDB.hmset(hash_name, value_dic)
			print 'Set Info Successfully'
			return True
		except Exception, error:
			logging.warning('Fail to set data!\n') 
			raise error


	def getHash(self, hash_name, optinal_keys=[]):
		try:
			if not optinal_keys:
				return self.residDB.hgetall(hash_name)
			else:
				return self.residDB.hmget(hash_name, optinal_keys)
		except Exception, error:
			logging.warning('Fail to get data form redis!')
			raise error


	def filterHashTimeKey(self,hash_name, chart_data=False, **kwargs):
		if kwargs.get('start') and kwargs.get('end'):
			start_key, end_key = kwargs['start'], kwargs['end']
		else:
			'''now time as end time and the 3 hours time before as start time '''
			delay = 2.5*3600
			local_time = time.time()
			end_key = time.strftime(TimeFormat, time.localtime(local_time))
			start_key = time.strftime(TimeFormat, time.localtime(local_time-delay))
		
		print start_key, end_key
		for position in xrange(1, len(start_key)):
			if start_key[position] != end_key[position]:
				break
		match_key = start_key[0:position] + '*'
		try: 
			hash_data = self.residDB.hscan(hash_name, 0, match_key, 1000)[1]
			keys = sorted(hash_data.keys())
# 			print keys, '\n', len(keys)
# 			print keys[]
			host_all_info = [json.loads(hash_data[key]) for key in keys if \
				  		key>=start_key and key<=end_key]
			if not chart_data:
				return host_all_info
			else:
				point_numb = 12
				infos = host_all_info[-point_numb:]
				info_dic = {'cpuUsage':[], 'cpuLoad':[],
							'memUsage':[], 'procNumb':[]}
				for info in infos:
					info_dic['cpuUsage'].append(info['cpu']['cpuUsage'])
					info_dic['cpuLoad'].append(info['cpu']['load'])
					info_dic['memUsage'].append(info['memory']['memUsage'])
					info_dic['procNumb'].append(info['proc']['procNumb'])
				
				return info_dic
				
				
		except Exception, error:
			logging.warning('Fail to filter data form redis!')
			raise error


	def delHashKey(self, hash_name, key):
		try:
			if self.residDB.hexiste(hash_name, key):
				self.residDB.hdel(hash_name, key)
				logging.info('Success to delete '+hash_name+' '+key)
				return True
			else:
				logging.warning('The key '+key+' is not in '+hash_name)
				return False
		except Exception, error:
			logging.warning('Fail to excute delete!')
			raise error



if __name__ == '__main__':
	obj = RedisHashOprt(HostIP, Port)
# 	t = time.strftime(TimeFormat, time.localtime())


# 	data = {'cpu':{'usage': 35}, 'memory':{'totle':1010101, 'usage':72}, 'disk':{'totle':19478204, 'usage':7900000}}
# 	print data['cpu']['usage']
	# jdata = json.dumps(data)
	# print t
	# print jdata
	# obj.setHash('local2', {t:jdata})
# 	a = obj.getHash('local2')
# 	b = a['2015-11-09-16:17:22']
# 	print b
# 	print type(b)
# 	c = json.loads(json.dumps(b))
# 	print c 
# 	print data['cpu']['usage']
	# obj.setHash('local2', {t:'monitor'+str(i)})

	# print t
	# for i in xrange(800):
	# 	t = time.strftime(TimeFormat, time.localtime())
	# 	obj.setHash('local2', {t:'monitor'+str(i)})
	# 	time.sleep(1)
	# print obj.getHash('local2')
	# print time.time()
# 	hosts_reids_info = obj.filterHashTimeKey('127.0.0.1',
# 								start = '2015-11-30-15:13:03', end ='2015-11-30-16:13:06')
	hosts_reids_info = obj.filterHashTimeKey('127.0.0.1')
	print hosts_reids_info
	print len(hosts_reids_info)

	# print obj.getHash('local2')
	# print obj.delHashKey('local2', 'user1')
	# print obj.getHash('local2', ['user1','user2'])
