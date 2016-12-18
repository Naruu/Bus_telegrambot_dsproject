#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TERM 200
#define MAX_LENGTH 10000
#define MAX_TEXT_LENGTH 100
#define STATION_NUMBERS 10

typedef struct{
    int stopId; //Á¤·ùÀå Id
    double remain_seat; //ºó ÁÂ¼® ¼ö
	}Bus;

typedef struct{
    int Id; //±âÁØ Á¤·ùÀåÀÇ Á¤·ùÀå Id
    int stationnum; //Á¤·ÄÇÒ Á¤·ùÀåÀÇ ¼ö
	    char *time; //½Ã°£´ë
    Bus gbus[MAX_TERM]; //Á¤·ùÀå struct
}BUS_TERM;


void FIND(Bus *gbus, Bus *range);
void insertion_sort(BUS *range);
void STRTOK(char *, BUS_TERM bus);

/*
 *getBusëŠ” í•´ë‹¹í•˜ëŠ” ë²„ìŠ¤ì˜ Idì˜ ì‹œê°„ ì •ë³´ë¥¼ ê°€ì§„ í…ìŠ¤íŠ¸ íŒŒì¼.
 *ID_í‰ì¼_ìƒí–‰.txt
 */

int main(int argc, char * argv[]){
    FILE *fp;
    char buffer[MAX_LENGTH];
    BUS_TERM  bus;
    BUS arr_bus[STATION_NUMBERS];
    
    fp = fopen(argv[1], "r");
    bus.time = argv[2];
    bus.gbus[0].stopId=argv[3]; //±âÁØÀÌ µÇ´Â Á¤·ùÀåµµ ÀÔ·Â ¹Ş¾Æ¾ßµÅ. 

    while(fgets(buffer, sizeof(buffer), stdin) != NULL){
        STRTOK(buffer, bus);
    }
    
    FIND(bus.gbus, arr_bus);
    insertion_sort(arr_bus);
    
    return 0;
}

//memcpy(&heap[i],&heap[i/2],sizeof(bus));

void FIND(Bus *gbus, Bus *range){
	int staitonId=gbus[0].stopId;
	int n, i=1;
	int start, end;
	
	while(stationId!=gbus[n].stopID) n++;
	if(n==1) start=n;
	else if(n==2) start=n-1;
	else start=n-2;
	
	if(n+2<=gbus[0].remain_seat) end=n+2;
	else if(n+1<=gbus[0].remain_seat) end=n+1;
	else end=n;
	
	range[0].remain_seat=end-start+1; //range[0]¿¡´Â Á¤·ÄÇÒ Á¤·ùÀåÀÇ ¼ö°¡ µé¾îÀÖ´Ù. 
	
	while(start<=end){
		memcpy(&range[i],&gbus[start],sizeof(BUS));
		i++;
		start++;
		}
	}

void insertion_sort(BUS *range){
	int i, j;
	BUS temp; 
	
	for(i=2;i<range[0].remain_seat+1;i++){
		memcpy(&temp, &range[i], sizeof(BUS));
		j=i-1;
		while(j>0 && range[j].remain_seat>temp.remain_seat){
			memcpy(&range[j+1], &range[j], sizeof(BUS));
			j--;
		}
		memcpy(&range[j+1], &temp, sizeof(BUS));
	}
}

void STRTOK(char *buffer, BUS_TERM bus){
    char *token;
    char *time;
    char sep[] = " ,-/";
    int n = 1, len;
    token  = strtok(buffer, sep);
    strncat(time,token,6);
    
    if(strcmp(time , bus.time) != 0)
        return;
    while(token != NULL){
        token = strtok(NULL, sep);
        len = strcspn("|", token);
        token[len] = '\0';
        bus.gbus[n].stopId = atoi(token);
        bus.gbus[n].remain_seat = atoi(token+len+1);
        printf("%d %d\n", bus.gbus[n].stopId, bus.gbus[n].remain_seat);
        n++;
        
    }
    bus.gbus[0].rmain_seat=n-1; //gbus[0]¿¡´Â Ã£´Â Á¤·ùÀå Id¿Í ³ë¼±ÀÇ ÃÑ Á¤·ùÀå ¼ö°¡ µé¾îÀÖ´Ù. 
}
