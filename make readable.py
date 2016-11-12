#-*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from urllib.request import urlopen
from time import sleep


f=open("C:\\Users\\Hye-lee\\Desktop\\project\\route20161105.txt", 'r')
g=open("C:\\Users\\Hye-lee\\Desktop\\project\\route20161105_nominee ID.txt", 'w')
h=open("C:\\Users\\Hye-lee\\Desktop\\project\\route20161105_nominee_info.txt", 'w')
data=f.read()

routeID=[]
route_info=[]
line_data=data.split('^')


for i in range(len(line_data)):
	ll_data=line_data[i].split('|')
	if(ll_data[2]!='13') : 
		routeID.append(ll_data[0])
		route_info.append(line_data[i])

str='\n'.join(routeID)
str_info='\n'.join(route_info)
g.write(str)
h.write(str_info)

f.close()
g.close()
h.close()