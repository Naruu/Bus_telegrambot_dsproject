#-*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from urllib.request import urlopen
from time import sleep, time
from datetime import datetime


f=open("C:\\Users\\Hye-lee\\Desktop\\project\\route20161105_shinchon_seat.txt", 'r', encoding="utf-8")
g=open("C:\\Users\\Hye-lee\\Desktop\\project\\shinchon_station.txt", 'r', encoding="utf-8")

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
	if(j==10) :	filename='2000_1'
	elif(j==11) : filename='2000_2'
	else : filename=r_line[j][1]
	save= 'C:\\Users\\Hye-lee\\Desktop\\project\\' + filename + '.txt'
	x=open(save, 'a', encoding="utf-8")
	
	if(j<=7) :
		key='VFNlqW0%2Bbbmd6fRfXsRI9UBvf3ZlFi7BkHlPlOCrC4%2BxQ8%2BKafexJ1XEOh%2F5pO7UycAqSl0Za0z%2FmTHOpWG7qA%3D%3D'
	else :
		key='SEmKkqAi1mRqIn6LSysvMM3ATeTEw5AhNMWF%2BfznsJNSPjZTiA3RPFjcVMdto5zpLR4FEM%2B%2BvnLU5AECi6dpKw%3D%3D'
	url='http://openapi.gbis.go.kr/ws/rest/buslocationservice?serviceKey='+ key + '&routeId=' + r_line[j][0]
	
	data = urlopen(url).read().decode('utf-8')
	root=ET.fromstring(data)
	
	for y in root.iter("resultCode") : resultCode=y.text
	if(resultCode=='0') :
		for bus in root.iter("busLocationList") :
			if(bus.find('remainSeatCnt').text=='-1') : message.append('x')
			else :
				index=s_ID.index(bus.find('stationId').text)
				if(s_line[index][2]=='정') : 
					up.append(bus.find('stationId').text + '|' + bus.find('remainSeatCnt').text)
				else : 
					down.append(bus.find('stationId').text + '|' + bus.find('remainSeatCnt').text)
		strup='/'.join(up)
		strdown='/'.join(down)
		message=root[1][0].text + '-'+ strup + '-' + strdown +'^'
		x.write(message)
	sleep(1)
	x.close()


while(1) :
	start=time()
	if ('10' in datetime.now().isoformat(' ')[11:13]) : break
	for n in range(1,16) :
		seat(n)
	
	end=time()
	delay=10*60-(end-start)
	sleep(delay)

f.close()
g.close()