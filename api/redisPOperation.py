# -*-coding:utf-8-*-
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
            self.residDB = redis.Redis(host=host_ip, port=port_numb, db=db_numb)
        except Exception, error:
            logging.warning('Fail to connet ' + HostIP + ' redis!')
            raise error

    def setHash(self, hash_name, value_dic):
        try:
            self.residDB.hmset(hash_name, value_dic)
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

    def filterHashTimeKey(self, hash_name, chart_data=False, **kwargs):
        if kwargs.get('start') and kwargs.get('end'):
            start_key, end_key = kwargs['start'], kwargs['end']
        else:
            '''now time as end time and the 3 hours time before as start time '''
            delay = 5 * 3600
            local_time = time.time()
            end_key = time.strftime(TimeFormat, time.localtime(local_time))
            start_key = time.strftime(TimeFormat, time.localtime(local_time - delay))

        for position in xrange(1, len(start_key)):
            if start_key[position] != end_key[position]:
                break
        match_key = start_key[0:position] + '*'

        try:
            hash_data = self.residDB.hscan(hash_name, 0, match_key, 1000)[1]
            keys = sorted(hash_data.keys())
            host_all_info = []
            host_all_keys = []
            for key in keys:
                if key >= start_key and key <= end_key:
                    host_all_info.append(json.loads(hash_data[key]))
                    host_all_keys.append(key)

            if not chart_data:
                return host_all_info
            else:
                point_numb = 12
                print len(host_all_info)
                if  len(host_all_info) > 12:
                    infos = host_all_info[-point_numb:]
                else:
                    point_numb = len(host_all_info)
                    infos = host_all_info

                info_dic = {'cpuUsage': [], 'cpuLoad': [],
                            'memUsage': [], 'procNumb': [],
                            'start': host_all_keys[-point_numb][-8:-3],
                            'end': host_all_keys[-1][-8:-3],
                            'host': hash_name}
                for info in infos:
                    info_dic['cpuUsage'].append(float(info['cpu']['cpuUsage'][:-1]))
                    info_dic['cpuLoad'].append(float(info['cpu']['load']))
                    info_dic['memUsage'].append(float(
                        info['memory']['memUsage'][:-1]))
                    info_dic['procNumb'].append(int(info['proc']['procNumb']))
                return info_dic

        except Exception, e:
            print str(e)
            logging.warning('Fail to filter data form redis!')
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
