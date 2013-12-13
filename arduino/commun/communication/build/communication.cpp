#include <Arduino.h>

int main(void)
{
	init();

#if defined(USBCON)
	USBDevice.attach();
#endif
	
	setup();
    
	for (;;) {
		loop();
		if (serialEventRun) serialEventRun();
	}
        
	return 0;
}

void setup();
void loop();
#line 1 "build/communication.ino"
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