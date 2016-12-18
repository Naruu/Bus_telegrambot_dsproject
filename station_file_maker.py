#-*-coding : utf-8 -*-

import text_handler

total_text=text_handler.handler('C:\\Users\\Hye-lee\\Desktop\\project\\shinchon_station.txt')

up=[]
down=[]
	
for i in range(len(total_text)-1) :
	if(total_text[i][0]==total_text[i+1][0]) :
		if(total_text[i][2]=='정') :
			up.append(total_text[i][1]+'_'+total_text[i][5][:-1])
		else : down.append(total_text[i][1]+'_'+total_text[i][5][:-1])
	else :
		down.append(total_text[i][1]+'_'+total_text[i][5][:-1])
		g=open('C:\\Users\\Hye-lee\\Desktop\\project\\stations\\' + 'st' +total_text[i][0] + '_'+ '0' '.txt','w')
		h=open('C:\\Users\\Hye-lee\\Desktop\\project\\stations\\' + 'st' +total_text[i][0] + '_'+ '1' '.txt','w')
		g.write('|'.join(up))
		h.write('|'.join(down))
		up=[]
		down=[]
		
down.append(total_text[i+1][1]+'_'+total_text[i+1][5][:-1])
g=open('C:\\Users\\Hye-lee\\Desktop\\project\\stations\\' + 'st' +total_text[i][0] + '_'+ '0' '.txt','w')
h=open('C:\\Users\\Hye-lee\\Desktop\\project\\stations\\' + 'st' +total_text[i][0] + '_'+ '1' '.txt','w')
g.write('|'.join(up))
h.write('|'.join(down))