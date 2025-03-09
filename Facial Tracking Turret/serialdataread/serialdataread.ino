#include <Servo.h>

Servo xServo;
Servo yServo;

int xPin = 9;   // X-axis servo pin
int yPin = 10;  // Y-axis servo pin

int xPos = 90;  // Initial positions
int yPos = 90;

void setup() {
  Serial.begin(9600);
  xServo.attach(xPin);
  yServo.attach(yPin);
  xServo.write(xPos);
  yServo.write(yPos);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');
    
    if (commaIndex > 0) {
      xPos = data.substring(0, commaIndex).toInt();
      yPos = data.substring(commaIndex+1).toInt();
      
      xPos = constrain(xPos, 0, 180);
      yPos = constrain(yPos, 0, 180);
      
      xServo.write(xPos);
      yServo.write(yPos);
    }
  }
}