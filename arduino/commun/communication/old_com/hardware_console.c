#include <stdio.h>
#include <string.h>

#include "hardware.h"


////////////////////
#define SERIAL_LOOPBACK_BUFFER_LENGTH 64
char serialLoopbackBuffer[SERIAL_LOOPBACK_BUFFER_LENGTH] = {0};
char serialLoopbackBufferBegin = 0, serialLoopbackBufferEnd = 0;

void printBinary(char* data, int n){
    for(char i=0; i<n; i++){
        for(char j=0; j<8; j++){
            if(data[i] & 0x80>>j)   putchar('1');
            else                    putchar('0');
        }
        putchar(' ');
    }
}

int serialPushLoopbackBuffer(char* data, char n){
    if( n==0 ) return 0;
    //printf("[DEBUG]push(%u) %u %u\n", n, serialLoopbackBufferBegin, serialLoopbackBufferEnd);
    if(n+serialLoopbackBufferEnd > SERIAL_LOOPBACK_BUFFER_LENGTH){
        if(n+serialLoopbackBufferEnd-serialLoopbackBufferBegin > SERIAL_LOOPBACK_BUFFER_LENGTH) return -1;
        char tmpwritten = SERIAL_LOOPBACK_BUFFER_LENGTH-serialLoopbackBufferEnd;
        memcpy(&(serialLoopbackBuffer[serialLoopbackBufferEnd]), data, tmpwritten);
        memcpy(serialLoopbackBuffer, &(data[tmpwritten]), n-tmpwritten);
        serialLoopbackBufferEnd = n-tmpwritten;
    }else{
        memcpy(&(serialLoopbackBuffer[serialLoopbackBufferEnd]), data, n);
        serialLoopbackBufferEnd += n;
    }
    return 0;
}

int serialReadLoopbackBuffer(char* data, char n){
    //printf("[DEBUG]read(%u) %u %u\n", n, serialLoopbackBufferBegin, serialLoopbackBufferEnd);
    char read = serialLoopbackBufferEnd - serialLoopbackBufferBegin;
    if(serialLoopbackBufferBegin > serialLoopbackBufferEnd) read += SERIAL_LOOPBACK_BUFFER_LENGTH;

    if( n < read ) read = n;
    if( read==0 ) return 0;
    if(serialLoopbackBufferBegin+read > SERIAL_LOOPBACK_BUFFER_LENGTH){
        char tmpread = SERIAL_LOOPBACK_BUFFER_LENGTH-serialLoopbackBufferBegin;
        memcpy(data, &(serialLoopbackBuffer[serialLoopbackBufferBegin]), tmpread);
        memcpy(&(data[tmpread]), serialPushLoopbackBuffer, n-tmpread);
        serialLoopbackBufferBegin = read-tmpread;
    }else{
        memcpy(data, &(serialLoopbackBuffer[serialLoopbackBufferBegin]), read);
        serialLoopbackBufferBegin += read;
    }
    return read;
}

////////////////////



int serialInit(){
    char debug[2];
    debug[0] = 0b11100000; debug[1]= 0b00011000;
    serialSend(debug, 2);
    debug[0] = 0b10000001; debug[1]= 0b00100100;
    serialSend(debug, 2);
    serialRead(debug, 5);
    serialRead(debug, 2);
    return 0;
}

void serialClose(){}


int serialRead(char* buffer, char n){
    if( n == (char)0 ) return -1;

    char r = serialReadLoopbackBuffer(buffer, n);
    printf("[READ(%hhu->%hhu)]: ", n, r);
    printBinary(buffer, r);
    printf("\n");

}


int serialSend(char* data, char n){
    if( n == (char)0 ) return -1;
    serialPushLoopbackBuffer(data, n);

    printf("[SEND(%hhu)]", n);
    printBinary(data, n );
    printf("\n");

    return 0;
}





