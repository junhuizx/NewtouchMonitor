# *-coding:utf-8-*-
import redis
import logging
import time
import json

# Target redis host ip and port
HostIP = '192.168.205.10'
Port = 6379
TimeFormat = '%Y-%m-%d-%X'


class RedisHashOprt(object):
    def __init__(self, host_ip, port_numb, db_numb=0):
        try:
            self.residDB = redis.Redis(host=host_ip, port=port_numb, db=db_numb)
            print 'dbsize:%s' % self.residDB.dbsize()
            print 'Connect Successfully!\nRedis--Version: ' + \
                  self.residDB.info()['redis_version']
        except Exception, error:
            logging.warning('Fail to connet ' + host_ip + ' redis!')
            raise error

    def setHash(self, hash_name, value_dic):
        try:
            self.residDB.hmset(hash_name, value_dic)
            print 'Set hash %s Info successfully' % hash_name
            return True
        except Exception, error:
            logging.warning('Fail to set % data!\n') % hash_name
            raise error

    def getHash(self, hash_name, optinal_keys=[]):
        ''' Returns a list of values ordered identically to optinal_keys '''
        try:
            if not optinal_keys:
                return self.residDB.hgetall(hash_name)
            else:
                return self.residDB.hmget(hash_name, optinal_keys)
        except Exception, error:
            logging.warning('Fail to get data form redis!')
            raise error

    def filterHashTimeKey(self, hash_name, keys_list):
        host_all_keys = []
        info_dic = {'cpuUsage': [], 'cpuLoad': [],
                    'memUsage': [], 'procNumb': [],
                    'host': hash_name}
        try:

            host_all_info = self.getHash(hash_name, keys_list)
            for pos, key in enumerate(keys_list):
                info = json.loads(host_all_info[pos])
                info_dic['cpuUsage'].append(float(info['cpu']['cpuUsage'][:-1]))
                info_dic['cpuLoad'].append(float(info['cpu']['load']))
                info_dic['memUsage'].append(float(info['memory']['memUsage'][:-1]))
                info_dic['procNumb'].append(int(info['proc']['procNumb']))
                host_all_keys.append(self.timeTransfer(key)[-8:-3])
            info_dic['times'] = host_all_keys
            return info_dic
        except:
            logging.warn('Fial to get data from hash %s' % hash_name)
            return {}

    def delHashKey(self, hash_name, key):
        try:
            if self.residDB.hexiste(hash_name, key):
                self.residDB.hdel(hash_name, key)
                logging.info('Success to delete ' + hash_name + ' ' + key)
                return True
            else:
                logging.warning('The key ' + key + ' is not in ' + hash_name)
                return False
        except Exception, error:
            logging.warning('Fail to excute delete!')
            raise error

    def setHashIndexList(self, list_name, value):
        if not self.residDB.exists(list_name):
            print 'New list: %s' % list_name
        try:
            self.residDB.lpush(list_name, value)
            print 'Set hash index list %s info successfully' % list_name
        except Exception, error:
            logging.warn('Fail to set list % data!\n' % list_name)
            raise error

    def getListValue(self, list_name, list_len=359, instance=True):
        if instance == True and self.residDB.exists(list_name):
            # 			print len(self.residDB.lrange(list_name, 0, 359))
            return self.residDB.lrange(list_name, 0, list_len)[0::30]
        else:
            return self.residDB.lrange(list_name, 0, list_len)
        logging.warn('No %s in redis!' % list_name)
        return []

    def getInstanceData(self, hash_name, keys_list):
        keys_list.reverse()
        if not keys_list or not self.residDB.exists(hash_name):
            return {}
        result = {'memUsage': [], 'disk': {}, 'diskName': []}
        info_list = self.getHash(hash_name, keys_list)
        result['times'] = [self.timeTransfer(key[0:8])[-8:-3] \
                           for key in keys_list]

        for obj in info_list:
            info = eval(obj)
            result['memUsage'].append(round(float(
                info['memstat']['used']) * 100 / float(
                info['memstat']['total']), 2))

            for disk in info['diskstat']:
                statistics = disk['statistics']
                if not result['disk'].get(disk['devname']):
                    result['diskName'].append(disk['devname'])
                    result['disk'][disk['devname']] = {
                        'kb_read': [self.sizeTransfer(statistics['kb_read'])],
                        'kb_write': [self.sizeTransfer(statistics['kb_write'])],
                        'speed_kb_read': [statistics['speed_kb_read']],
                        'speed_kb_write': [statistics['speed_kb_write']],
                        'tps': [statistics['tps']]}

                else:
                    result['disk'][disk['devname']]['kb_read'].append(
                        self.sizeTransfer(statistics['kb_read']))
                    result['disk'][disk['devname']]['kb_write'].append(
                        self.sizeTransfer(statistics['kb_write']))
                    result['disk'][disk['devname']]['speed_kb_read'].append(
                        statistics['speed_kb_read'])
                    result['disk'][disk['devname']]['speed_kb_write'].append(
                        statistics['speed_kb_write'])
                    result['disk'][disk['devname']]['tps'].append(
                        statistics['tps'])

        return result

    @staticmethod
    def timeTransfer(offset_str):
        return time.strftime(TimeFormat, time.localtime(int(offset_str, 16)))
    
    @staticmethod
    def sizeTransfer(size_numb):
        return round(float(size_numb)/1024)


if __name__ == '__main__':
    list_name = 'list-a:172.16.17.110-h:127.0.0.1'
    hash_name = 'hash-a:172.16.17.110-h:127.0.0.1'
    host = '192.168.205.10'
    obj = RedisHashOprt('localhost', Port, 0)
    keys = obj.getListValue(list_name, 11, instance=False)
    print keys
    value = obj.filterHashTimeKey(hash_name, keys)
    print value

    print len(obj.getHash(hash_name, keys))
# value = hex(int(time.mktime(time.localtime())))[2:]
# 	print value
# 	obj.setHashIndexList(list_name, value)
# 	obj = RedisHashOprt('127.9.9.9', Port)
# 	t = time.strftime(TimeFormat, time.localtime())
# 	'565fde39-7a95-fa36-0a3c80c3'


# 	list_name = "list:70faf7f6-7f1d-45d6-8a84-c062ec1af997"
# 	keys_list = obj.getListValue(list_name)
# 	print keys_list
# 	print len(keys_list)
# 	print obj.getHash('hash_data', data_list[0])
# 	print len( obj.getHash('hash_data', data_list))
# 	print obj.timeTransfer('565fc390')
# 	print obj.getInstanceData('hash_data', keys_list)

#  	data = {'cpu':{'usage': 35}, 'memory':{'totle':1010101, 'usage':72}, 'disk':{'totle':19478204, 'usage':7900000}}

#  	hosts_reids_info = obj.filterHashTimeKey('127.0.0.1',
#  					   start = '2015-11-30-15:13:03', end ='2015-11-30-17:33:06',chart_data= True)
#  	hosts_reids_info = obj.filterHashTimeKey('127.0.0.1')
#  	print hosts_reids_info
#  	print len(hosts_reids_info)
