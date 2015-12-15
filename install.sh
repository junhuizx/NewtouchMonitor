#!/usr/bin/env bash
rm -rf /usr/share/NewtouchMonitor/api_bak
rm -rf /usr/share/NewtouchMonitor/dashboard_bak
rm -rf /usr/share/NewtouchMonitor/static_bak
rm -rf /usr/share/NewtouchMonitor/templates_bak

mv /usr/share/NewtouchMonitor/api /usr/share/NewtouchMonitor/api_bak
mv /usr/share/NewtouchMonitor/dashboard /usr/share/NewtouchMonitor/dashboard_bak
mv /usr/share/NewtouchMonitor/static /usr/share/NewtouchMonitor/static_bak
mv /usr/share/NewtouchMonitor/templates /usr/share/NewtouchMonitor/templates_bak

cp -rf api /usr/share/NewtouchMonitor/
cp -rf dashboard /usr/share/NewtouchMonitor/
cp -rf static /usr/share/NewtouchMonitor/
cp -rf templates /usr/share/NewtouchMonitor/

service apache2 restart