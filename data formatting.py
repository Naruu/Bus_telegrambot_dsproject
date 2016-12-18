#-*-coding : utf-8 -*-

from datetime import date, time, datetime
from time import strptime
from pandas import Series,DataFrame

routeId=[]
routeName=[]

# 신촌에 정차하는 버스 노선 정보가 담긴 파일을 읽고 노선ID, 노선 이름을 return한다.
def route() :
	r=g=open("C:\\Users\\Hye-lee\\Desktop\\project\\route20161105_shinchon_seat.txt", 'r', encoding='utf-8')
	lines=r.readlines()
	for line in lines :
		line=line.split('|')
		routeId.append(line[0])
		routeName.append(line[1])
	return (routeId, routeName)

# list 안에 list가 있는 경우 하나의 list로 바꾼다.
def untie(list) :
	L=[]
	for i in range(len(list)) :
		for j in range(len(list[i])) :
			L.append(list[i][j])
	return L
	
# 노선별 정류장 정보가 들어있는 파일(shinchon_station.txt)을 읽고 상행 때 지나가는 정류장, 역행 때 지나가는 정류장을 나누어 저장한다.
# 입력이 up이면 상행, down이면 하행이 때 지나가는 정류장의 목록을 return한다.
def findUpDown(updown, n) :
	stationId=routeId[n]
	if(updown=='up') : updown='정'
	else : updown='역'
	
	g=open("C:\\Users\\Hye-lee\\Desktop\\project\\shinchon_station.txt", 'r', encoding='utf-8')
	lines=g.readlines()
	Lstation=[]
	for line in lines :
		line=line.split('|')
		if(line[0]==stationId) :
			if(line[2]==updown) : Lstation.append(line[1])
	
	g.close()
	
	return Lstation
	
# 표(Datframe)과 목록을 받아 표에서 목록에 들어 있는 열을 제거한다.
# 즉, 상행의 정류장 목록을 받으면 표에서 상행 정류장을 제거해 하행 때 지나가는 정류장만으로 구성된 표를 만든다.
def sieve(A, L) :
	sieved=A.copy()
	
	for station in L :
		if(station not in sieved.columns) : continue
		sieved=sieved.drop(station, axis=1)
	return sieved
	
# 표(Dataframe)을 text file에 일정 형식을 저장한다.
# 파일 이름 : 노선ID_0.txt(상행), 노선ID_1.txt(하행)
# 출력 형식 : 시간 - 정류장ID_빈좌석수/정류장ID_/빈좌석수 ...
def printData(A, i, n) :
	h=open("C:\\Users\\Hye-lee\\Desktop\\project\\PrintData\\" + str(routeId[n]) + "_" + str(i) + ".txt", 'a', encoding='utf-8')
	
	for index, row in A.iterrows() :
		LL=[]
		L=[]
		for station, seat in row.iteritems() :
			L.append(str(station) + '|' + str(seat))
		LL.append(str(index.hour) + ':' + str(index.minute) + '-' + '/'.join(L))
		h.write(str(LL[0]))
		h.write('\n')
	
	h.close()	


def text(n):
	# 10분마다 파싱한 데이터가 저장된 파일을 읽어온다.
	f=open("C:\\Users\\Hye-lee\\Desktop\\project\\DATA\\" + str(routeName[n])+ ".txt", 'r')

	lines=f.read().split('^')
	lines=lines[:-1]
	
	RawData=DataFrame(columns=("date", "time", "data"))
	
	for line in lines :
		when=line[:16]
		data=line[25:]
		station=data.split('/')
	
		w=datetime.strptime(when,"%Y-%m-%d %H:%M")
		ymd=date(w.year, w.month, w.day)
		t00=time(w.hour, 00)
		t30=time(w.hour, 30)

		# 모든 데이터를 0분~30분, 30분~0분으로 분류하여 표로 만든다.
		if(w.minute<30) :
			data00=[]
			for j in range(len(station)) :
				data00.append(station[j])
			RawData.loc[len(RawData)]=(ymd,t00,data00)
		else :
			data30=[]
			for j in range(len(station)) :
				data30.append(station[j])
			RawData.loc[len(RawData)]=(ymd,t30,data30)
	
	# 다른 날짜, 같은 시간대끼리 합한다. (ex. 11월 27일 12:00, 11월 28일 12:00 합침)
	T=RawData.groupby('time')['data'].apply(lambda x: list(x))

	L=[]
	LL=[]
	for i in range(len(T)) :
		L=untie(T[i])
		LL.append(L)
	DbtimeList=Series(LL, index=T.index)
	
	# 시간대로 정리된 데이터를 정류장 별로도 정리하여 표를 만든다.
	# 행은 정류장ID, 열은 시간대이고, 각 셀에는 평균 빈좌석 수가 들어있다.
	SS=[]
	for i in range(len(DbtimeList)) :
		Lstation=[]
		Lseat=[]
		for j in range(len(DbtimeList[i])) :
			sspair=DbtimeList[i][j].split('|')
			if(len(sspair)<2) : continue
			Lstation.append(str(sspair[0]))
			Lseat.append(int(sspair[1]))
		S=Series(Lseat, index=Lstation)
		Smeaned=S.groupby(S.index).mean().round(2)
		SS.append(Smeaned)
	
	# 빈 좌석 정보가 없는 경우 0을 넣는다.
	TimebyData=DataFrame(SS)
	TimebyData.index=DbtimeList.index
	TimebyData=TimebyData.fillna(0)
	
	# 상행,하행 때 지나가는 정류장 목록을 만든다.
	up=findUpDown('up', n)
	down=findUpDown('down',n)[:-1]
	
	# 원래의 표를 복사하여 상행에서의 표, 하행에서의 표로 만든다.
	UpData=sieve(TimebyData, down)
	DownData=sieve(TimebyData, up)
	
	# 상행에서의 표, 하행에서의 text file로 출력한다.
	printData(UpData, 0, n)
	printData(DownData, 1, n)
	
	#UpData.to_csv('C:\\Users\\Hye-lee\\Desktop\\UpData.csv')
	#DownData.to_csv('C:\\Users\\Hye-lee\\Desktop\\DownData.csv')
	#TimebyData.to_csv('C:\\Users\\Hye-lee\\Desktop\\TimebyData.csv')
	f.close()
	
	
route()
for n in range(15) : 
	text(n)