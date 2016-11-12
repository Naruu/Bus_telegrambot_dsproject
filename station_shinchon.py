#-*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from urllib.request import urlopen
from time import sleep


f=open("C:\\Users\\Hye-lee\\Desktop\\project\\routestation20161105.txt", 'r')
g=open("C:\\Users\\Hye-lee\\Desktop\\project\\routeID.txt", 'r')
h=open("C:\\Users\\Hye-lee\\Desktop\\project\\shinchon_station.txt", 'w')

data=f.read().split('^')
routeID=g.read().split('/')

line=[]

for ID in routeID :
	for i in range(0, len(data)) :
		mline=data[i].split('|')
		if(mline[0]==ID) :
			line.append('|'.join(mline))
h.write('\n'.join(line))

"""
for i in range(len(line_data)):
	ll_data=line_data[i].split('|')
	if(ll_data[2]) : 
		routeID.append(ll_data[0])
		route_info.append(line_data[i])

str='\n'.join(routeID)
str_info='\n'.join(route_info)
g.write(str)
h.write(str_info)
"""

f.close()
g.close()
h.close()