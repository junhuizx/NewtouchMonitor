import json
from django import template

register = template.Library()

@register.filter
def memory_dict(dictionary):
    total = dictionary.get('total')
    used = dictionary.get('used')

    return '%sMB/%sMB' %(used, total)

@register.filter
def disk_speed_list(dictionary):
    disks = []
    for disk in dictionary:
        disk_name = disk['devname']
        disk_read_speed = disk['statistics']['speed_kb_read']
        disk_write_speed = disk['statistics']['speed_kb_write']

    return ""

@register.filter
def disk_total_list(dictionary):
    disks = []


    return ""