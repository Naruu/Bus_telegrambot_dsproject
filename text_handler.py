#-*-coding : utf-8 -*-

def handler(file_name):
	f=open(file_name, 'r', encoding='utf-8')
	total=[]
	lines=f.readlines()
	for line in lines :
		total.append(line.split('|'))
	return total