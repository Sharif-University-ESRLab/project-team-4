int ledPin = 2;
String str;
int x;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  delay(10);
  
  int val = analogRead(0);
  Serial.println(val);

  
  if (Serial.available() > 0) {
    str = Serial.readStringUntil('\n');
    x = Serial.parseInt();
    analogWrite(ledPin, x / 4); 
    // analogRead values go from 0 to 1023, analogWrite values from 0 to 255
  }
}
