#include "Arduino.h"
#include "defines.h"
#include "defines_size.c"


void setup()
{
	Serial.begin(115200);
	initSize();
	
}

void loop()
{
	delay(1000);
	Serial.println(ordreSize[PINGPING]);
	Serial.println(ordreSize[A_GOTOR]);
}