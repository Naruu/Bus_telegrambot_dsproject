#-*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from urllib.request import urlopen
from time import sleep

f=open("C:\\Users\\Hye-lee\\Desktop\\project\\route20161105_shinchon_seat.txt", 'r')
g=open("C:\\Users\\Hye-lee\\Desktop\\project\\shinchon_station.txt", 'r')

r_lines=f.readlines()
s_lines=g.readlines()

def neat(l) :
	neat_l=[]
	for i in range(0, len(l)) :
		ll=l[i].split('|')
		neat_l.append(ll)
	return neat_l


r_line=neat(r_lines)
s_line=neat(s_lines)

s_ID=[]
for i in range(0,len(s_line)) :
	s_ID.append(s_line[i][1])

	
def seat(j) :
	up=[]
	down=[]
	message=[]
	save="C:\\Users\\Hye-lee\\Desktop\\project\\" + r_line[j][1] + '.txt'
	x=open(save, 'a')
	url='http://openapi.gbis.go.kr/ws/rest/buslocationservice?serviceKey=1234567890&routeId=' + r_line[j][0]
	data = urlopen(url).read().decode('utf-8')
	root=ET.fromstring(data)
	if((root[1][1].text)=='0') :
		for bus in root.iter("busLocationList") :
			if(bus.find('remainSeatCnt').text=='-1') :
				message.append('-00') # cannot remove the list 'message'?
			else :
				index=s_ID.index(bus.find('stationId').text)
				if(s_line[index][2]=='정') : 
					up.append(bus.find('stationId').text + '|' + bus.find('remainSeatCnt').text)
				else : 
					down.append(bus.find('stationId').text + '|' + bus.find('remainSeatCnt').text)
	strup='/'.join(up)
	strdown='/'.join(down)
	message=root[1][0].text + '-'+ strup + '-' + strdown 
	x.write(message)
	sleep(1) # managing time! Time issue!!
	x.close()
	
seat(1)
#bus 2000 should have two distinct files.

f.close()
g.close()
