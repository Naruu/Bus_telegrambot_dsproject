#-*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from urllib.request import urlopen
from time import sleep, time
from datetime import datetime
from sys import exit


# 읽어온 파일을 다루기 쉽도록 tokenize
def neat(l) :
	neat_l=[]
	for i in range(0, len(l)) :
		ll=l[i].split('|')
		neat_l.append(ll)
	return neat_l

# route20161105_shinchon_seat.txt 신촌을 지나는 광역 버스 노선 목록이 담긴 text file
# shinchon_station.txt 신촌을 지나가는 버스 노선의 총 정류장 목록이 담긴 text file	
f=open("/home/pi/ds_parser/route20161105_shinchon_seat.txt", 'r', encoding="utf-8")
g=open("/home/pi/ds_parser/shinchon_station.txt", 'r', encoding="utf-8")

r_lines=f.readlines()
s_lines=g.readlines()

# s_ID : 정류장ID 목록
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
	# 파싱한 데이터를 노선 번호로 text file에 저장
	save= '/home/pi/ds_parser/FILES/' + filename + '.txt'
	x=open(save, 'a', encoding="utf-8")
	
	if(j<=7) :
		key='VFNlqW0%2Bbbmd6fRfXsRI9UBvf3ZlFi7BkHlPlOCrC4%2BxQ8%2BKafexJ1XEOh%2F5pO7UycAqSl0Za0z%2FmTHOpWG7qA%3D%3D'
	else :
		key='SEmKkqAi1mRqIn6LSysvMM3ATeTEw5AhNMWF%2BfznsJNSPjZTiA3RPFjcVMdto5zpLR4FEM%2B%2BvnLU5AECi6dpKw%3D%3D'
	url='http://openapi.gbis.go.kr/ws/rest/buslocationservice?serviceKey='+ key + '&routeId=' + r_line[j][0]
	
	# api에 접속하여 xml을 읽어서 root에 저장.
	data = urlopen(url).read().decode('utf-8')
	root=ET.fromstring(data)
	
	for y in root.iter("resultCode") : resultCode=y.text
	if(resultCode=='0') : # api가 정상적으로 작동할 때
		for bus in root.iter("busLocationList") :
			if(bus.find('remainSeatCnt').text=='-1') : message.append('x') # 빈 좌석 정보를 제공하지 않으연 x 표시
			else :
				index=s_ID.index(bus.find('stationId').text)
				if(s_line[index][2]=='정') : # 상행 정류장이면
					up.append(bus.find('stationId').text + '|' + bus.find('remainSeatCnt').text)
				else : # 하행 정류장이면
					down.append(bus.find('stationId').text + '|' + bus.find('remainSeatCnt').text)
		# 정류장은 /로, 시간은 ^로 표시하여 구분
		strup='/'.join(up)
		strdown='/'.join(down)
		# 시간 - 상행 - 하행 형식으로 저장
		message=root[1][0].text + '-'+ strup + '-' + strdown +'^'
		x.write(message)
	
	# 서버 부하를 막기 위해 sleep
	sleep(1)
	x.close()


for n in range(16) :
	seat(n)

f.close()
g.close()
exit()