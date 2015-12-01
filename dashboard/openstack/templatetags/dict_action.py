import json
from django import template

register = template.Library()

def formatsize(level):
    if level == 0:
        return "BYTE"
    elif level == 1:
        return "KB"
    elif level == 2:
        return "MB"
    elif level == 3:
        return "GB"
    elif level == 4:
        return "TB"
    else:
        return ""

@register.filter
def memory_dict(dictionary):
    total_level = 2
    used_level = 2

    total = int(dictionary.get('total'))
    while total >= 1024:
        total = total / 1024.00
        total_level += 1
    total = "%.2f" % (total)

    used = int(dictionary.get('used'))
    while used >= 1024:
        used = used / 1024.00
        used_level += 1
    used = "%.2f" % (used)

    return '%s%s / %s%s' %(used, formatsize(used_level), total, formatsize(total_level))

@register.filter
def disk_speed_list(list):
    disks_speed = ""
    for disk in list:
        disk_name = disk['devname']
        disk_read_speed = disk['statistics']['speed_kb_read']
        disk_write_speed = disk['statistics']['speed_kb_write']
        disks_speed += "%s : %sKB/s / %sKB/s\n" % (disk_name, disk_read_speed, disk_write_speed)

    return disks_speed

@register.filter
def disk_total_list(list):
    disks_total = ""
    for disk in list:
        disk_name = disk['devname']
        read_level = 1
        write_level = 1

        disk_read_total = int(disk['statistics']['kb_read'])
        while disk_read_total >= 1024:
            disk_read_total = disk_read_total / 1024.00
            read_level += 1
        disk_read_total = "%.2f" % (disk_read_total)

        disk_write_total = int(disk['statistics']['kb_write'])
        while disk_write_total >= 1024:
            disk_write_total = disk_write_total / 1024.00
            write_level += 1
        disk_write_total = "%.2f" % (disk_write_total)

        disks_total += "%s : %s%s / %s%s\n" % (disk_name, disk_read_total, formatsize(read_level), disk_write_total, formatsize(write_level))

    return disks_total

@register.filter
def network_total_list(list):
    network_total = ""
    for network in list:
        net_devname = network['devname']
        receive_level = 0
        transmit_level = 0

        net_receive_bytes = network['receive']['bytes']
        while net_receive_bytes >= 1024:
            net_receive_bytes = net_receive_bytes / 1024.00
            receive_level += 1
        net_receive_bytes = "%.2f" % (net_receive_bytes)

        net_transmit_bytes = network['transmit']['bytes']
        while net_transmit_bytes >= 1024:
            net_transmit_bytes = net_transmit_bytes / 1024.00
            transmit_level += 1
        net_transmit_bytes = "%.2f" % (net_transmit_bytes)

        network_total += "%s : %s%s / %s%s\n" % (net_devname, net_receive_bytes, formatsize(receive_level), net_transmit_bytes, formatsize(transmit_level))

    return network_total

