#include <Arduino.h>
#include <Servo.h>

#define PIN_SERVO 43

Servo s;
void setup(){
	s.attach(PIN_SERVO);
}

void loop() {
	int i;
	for (i=150; i>=75; i-=5) {
		s.write(i);
		delay(3000);
	}
}
