import json
from django import template

register = template.Library()

@register.filter
def syslog_message(message):
    return_message = ''
    tag, sep, message  = message.partition(":")

    if (-1 != tag.find("message repeated")):
        message = message.strip().lstrip("[").rstrip("]")
        tag, sep, message = message.partition(":")

    type = tag.strip().lstrip("%%10")
    type = type.split("/", 1)[0]
    return_message += 'Type : %s\n' % (type)

    message_list = message.split(";")
    for message in message_list:
        return_message += '%s\n'% (message)

    return return_message
