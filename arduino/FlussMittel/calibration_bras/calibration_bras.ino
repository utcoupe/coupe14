#include <Arduino.h>
#include <Servo.h>

#define PIN_SERVO

Servo s;
void setup(){
	s.attach(PIN_SERVO);
}

void loop() {
	int i;
	for (i=0; i<180; i+=10) {
		s.write(i);
		delay(10);
	}
}
