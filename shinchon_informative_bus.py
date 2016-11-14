#-*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from urllib.request import urlopen
from time import sleep


f=open("C:\\Users\\Hye-lee\\Desktop\\project\\route20161105_nominee_info.txt", 'r')
g=open("C:\\Users\\Hye-lee\\Desktop\\project\\shinchon_bus2.txt", 'r')
h=open("C:\\Users\\Hye-lee\\Desktop\\project\\route20161105_shinchon_seat2.txt", 'a')


lines=f.readlines()
line=[]
info=[]
shinchon=[]
routeID=[]

p=0
b=0
for i in range(1, len(lines)) :
	mline=lines[i].split('|')
	line.append(mline)

s=g.readlines()
for sh in s :
	shinchon.append(sh[:-1])


for bus_num in shinchon :
	for j in range(len(line)) :
		if(line[j][1]==bus_num) :
			url='http://openapi.gbis.go.kr/ws/rest/buslocationservice?serviceKey=1234567890&routeId=' + line[j][0]
			data = urlopen(url).read().decode('utf-8')
			root=ET.fromstring(data)
			if((root[1][1].text)=='0') :
				for seat in root.iter("remainSeatCnt") :
					if(seat.text=='-1') :
						print(bus_num, "no information")
						b=b+1
						break
					else :
						p=p+1
						info.append('%d.' %p + ' ' + lines[j+1])
						routeID.append(line[j][0])
						break
			sleep(1)

print(b)
h.write('\n'.join(info))
h.write("\n\n number of possible bus lines is %d" %p)


"""
seat=[]
#for i in range(len(routeID)) : 
    url='http://openapi.gbis.go.kr/ws/rest/buslocationservice?serviceKey=1234567890&routeId=' + '200000115'
    data = urlopen(url).read().decode('utf-8')
    root=ET.fromstring(data)
    for remainseat in root.iter("remainSeatCnt") :
        seat.append(remainseat.text)
        sleep(1)

"""
        
f.close()
g.close()
h.close()