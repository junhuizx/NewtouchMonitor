class HostInfo(object):
    
    def __init__(self, info_dict):
        self.server = info_dict['server']
        
        
        self.procNumb = info_dict['proc']['procNumb'] if\
                        info_dict['proc'] else ''
                        
                        
        if info_dict['interface']:  
            self.interface = info_dict['interface'] if info_dict['interface']\
                             else []
            self.inTotal, self.outTotal = 0, 0
            for intf in self.interface:
                self.inTotal += int(intf[1])
                self.outTotal += int(intf[2])
            
        if info_dict['cpu']:
            self.cpuUsage = info_dict['cpu']['cpuUsage']
            self.cpuLoad = info_dict['cpu']['load']
            
        if info_dict['memory']:
            self.memTotal = info_dict['memory']['memTotal']
            self.memUsed = info_dict['memory']['memUsed']
            self.memUsage = info_dict['memory']['memUsage']
        
        if info_dict['load']:
            self.load5 = info_dict['load']['load5']
            self.load10 = info_dict['load']['load10']
            self.load15 = info_dict['load']['load15']

        if info_dict['disk']:
            self.diskDevice = info_dict['disk']['diskDevice']
            self.diskTotal = info_dict['disk']['diskTotal']
            self.diskUsed = info_dict['disk']['diskUsed']
            self.diskUsage = info_dict['disk']['diskUsage']
