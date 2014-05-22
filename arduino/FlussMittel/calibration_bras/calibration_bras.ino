#include <Arduino.h>
#include <Servo.h>

#define PIN_SERVO 43

Servo s;
void setup(){
	s.attach(PIN_SERVO);
}

void loop() {
	int i;
	s.write(150);
	/*
	for (i=180; i>=0; i-=10) {
		s.write(i);
		delay(1000);
	}*/
}
