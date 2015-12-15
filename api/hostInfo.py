class HostInfo(object):
    
    def __init__(self, info_dict):
        self.server = info_dict['server']
        self.agent = info_dict['agent']
        if 2 == len(info_dict.keys()):
            self.error = True
            return

        self.procNumb = info_dict['proc']['procNumb'] if\
                        info_dict['proc'] else ''
                        
                        
        if info_dict.get('interface', False):  
            self.interface = info_dict['interface'] if info_dict['interface']\
                             else []
            self.inTotal, self.outTotal = 0, 0
            for intf in self.interface:
                self.inTotal += int(intf[1])
                self.outTotal += int(intf[2])
            
        if info_dict.get('cpu', False):
            self.cpuUsage = info_dict['cpu']['cpuUsage']
            self.cpuLoad = info_dict['cpu']['load']
            
        if info_dict.get('memory', False):
            self.memTotal = info_dict['memory']['memTotal']
            self.memUsed = info_dict['memory']['memUsed']
            self.memUsage = info_dict['memory']['memUsage']
        
        if info_dict.get('load', False):
            self.load5 = info_dict['load']['load5']
            self.load10 = info_dict['load']['load10']
            self.load15 = info_dict['load']['load15']

        if info_dict.get('disk', False):
            self.diskDevice = info_dict['disk']['diskDevice']
            self.diskTotal = info_dict['disk']['diskTotal']
            self.diskUsed = info_dict['disk']['diskUsed']
            self.diskUsage = info_dict['disk']['diskUsage']


class HostNetInfo(object):
    def __init__(self, info_dic):
        if info_dic:
            self.name = info_dic.get('name', 'None')
            self.status = info_dic.get('status', 'None')
            self.instance_name =info_dic.get('instance_name', 'None')
            self.hypervisor_hostname = info_dic.get('hypervisor_hostname', 'None')
            
            self.addresses = info_dic.get('addresses', False)
            if self.addresses and isinstance(self.addresses, dict):
                self.fixed = self.addresses.get('fixed', 'None')
                self.floating = self.addresses.get('floating', 'None')
                self.floating_status = self.addresses.get('floating_status', 'None')
            else:
                self.fixed = 'None'    
                self.floating = 'None'
                self.floating_status = 'None'
            
            
        